import 'dart:async';
import 'dart:ui';
import 'dart:io';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import '../utils/l10n.dart';
import 'package:flutter/services.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api/phim_api.dart';
import '../api/firebase_api.dart';
import '../api/auth_api.dart';
import '../api/comment_api.dart';
import '../api/torrentio_api.dart';
import '../models/movie.dart';
import '../models/comment.dart';
import 'player_screen.dart';
import '../widgets/glass_search_bar.dart';
import '../utils/ui_utils.dart';
import '../widgets/glass_container.dart';
import '../widgets/custom_title_bar.dart';
import 'actor_detail_screen.dart';
import '../widgets/image_gallery_viewer.dart';

class MovieDetailScreen extends StatefulWidget {
  final String slug;
  final String? heroTag;
  final Movie? initialMovie;

  const MovieDetailScreen({
    super.key,
    required this.slug,
    this.heroTag,
    this.initialMovie,
  });

  @override
  State<MovieDetailScreen> createState() => _MovieDetailScreenState();
}

class _MovieDetailScreenState extends State<MovieDetailScreen> {
  Movie? _movie;
  bool _isLoading = true;
  StreamSubscription<Movie>? _movieSubscription;

  // Trailer state
  bool _isLoadingTrailer = false;
  bool _trailerNotFound = false;
  List<Map<String, String>> _actors = [];
  Timer? _autoPlayTimer;

  // Inline Trailer
  final _webviewController = WebviewController();
  bool _isWebviewInitialized = false;
  HttpServer? _trailerServer;
  int _trailerPort = 0;
  bool _showInlineTrailer = false;
  bool _trailerEnded = false;
  bool _isTrailerExpanded = false;
  bool _isTrailerPaused = false;
  bool _autoPlayTrailerSetting = true;
  String? _tmdbRating;
  double _averageRating = 0.0;
  int _totalRatings = 0;
  int _userRating = 0;
  int _hoverRating = 0;
  bool _isSubmittingRating = false;
  bool _isInWatchlist = false;

  // Server categorizations
  final List<EpisodeServer> _premiumServers = [];
  final List<EpisodeServer> _p2pServers = [];
  final List<EpisodeServer> _vietsubServers = [];
  final List<EpisodeServer> _tmServers = [];

  // Tab Selection State
  String _activeMainTab = 'Promax'; // 'Promax' or 'Standard'
  String _activeStandardSubTab = 'Vietsub'; // 'Vietsub' or 'Thuyết Minh'
  EpisodeServer? _currentServer;

  // P2P TV Series State
  int? _selectedSeason;
  Episode? _selectedP2pEpisode;
  bool _isFetchingP2pStreams = false;
  List<Episode> _p2pStreams = [];

  // Comments state
  List<Comment> _comments = [];
  bool _isLoadingComments = true;
  int _visibleComments = 5;
  final TextEditingController _commentController = TextEditingController();
  Map<String, String>? _currentUser;
  bool _isSubmittingComment = false;
  String? _replyingTo;
  final TextEditingController _replyController = TextEditingController();
  bool _isSubmittingReply = false;

  @override
  void initState() {
    super.initState();
    _loadSettings();
    _fetchDetail();
    _fetchFirebaseRatings();
    _loadUserAndComments();
    _checkWatchlistStatus();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    if (mounted) {
      setState(() {
        _autoPlayTrailerSetting = prefs.getBool('auto_play_trailer') ?? true;
      });
    }
  }

  Future<void> _checkWatchlistStatus() async {
    final isInWatchlist = await FirebaseApi.isInWatchlist(widget.slug);
    if (mounted) {
      setState(() {
        _isInWatchlist = isInWatchlist;
      });
    }
  }

  Future<void> _toggleWatchlist() async {
    if (_movie == null) return;
    if (_isInWatchlist) {
      await FirebaseApi.removeFromWatchlist(widget.slug);
      if (mounted) {
        setState(() => _isInWatchlist = false);
        UIUtils.showCustomSnackBar(context, L10n.t('removed_favorite'));
      }
    } else {
      final success = await FirebaseApi.addToWatchlist(_movie!);
      if (mounted) {
        if (success) {
          setState(() => _isInWatchlist = true);
          UIUtils.showCustomSnackBar(
            context,
            L10n.t('added_favorite'),
          );
        } else {
          UIUtils.showCustomSnackBar(
            context,
            L10n.t('favorite_full'),
            isError: true,
          );
        }
      }
    }
  }

  Future<void> _loadUserAndComments() async {
    final user = await AuthApi.getCurrentUser();
    final comments = await CommentApi.fetchComments(widget.slug);
    if (mounted) {
      setState(() {
        _currentUser = user;
        _comments = comments;
        _isLoadingComments = false;
      });
    }
  }

  Future<void> _fetchFirebaseRatings() async {
    final slug = widget.slug;
    final avgData = await FirebaseApi.getAverageRating(slug);
    final userScore = await FirebaseApi.getUserRating(slug);
    if (mounted) {
      setState(() {
        _averageRating = avgData['average'];
        _totalRatings = avgData['count'];
        _userRating = userScore;
      });
    }
  }

  @override
  void dispose() {
    _movieSubscription?.cancel();
    _autoPlayTimer?.cancel();
    _trailerServer?.close(force: true);
    if (_isWebviewInitialized) {
      _webviewController.dispose();
    }
    _commentController.dispose();
    _replyController.dispose();
    super.dispose();
  }

  Future<void> _pauseTrailer() async {
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "if(player && player.pauseVideo) { player.pauseVideo(); }",
        );
      } catch (e) {}
    }
    if (mounted) {
      setState(() {
        _showInlineTrailer = false;
        _isTrailerPaused = true;
        _isTrailerExpanded = false;
      });
    }
  }

  void _playTrailer() {
    if (_isWebviewInitialized) {
      _webviewController.executeScript(
        "if(player && player.playVideo) { player.seekTo(0); player.playVideo(); }",
      );
      setState(() {
        _showInlineTrailer = true;
        _isTrailerPaused = false;
        _trailerEnded = false;
        _isTrailerExpanded = false;
      });
    } else {
      _startInlineTrailer();
    }
  }

  void _resumeTrailer() {
    if (_isWebviewInitialized) {
      _webviewController.executeScript(
        "if(player && player.playVideo) { player.playVideo(); }",
      );
      setState(() {
        _showInlineTrailer = true;
        _isTrailerPaused = false;
        _trailerEnded = false;
        _isTrailerExpanded = false;
      });
    }
  }

  void _fetchDetail() {
    _movieSubscription =
        PhimApi.fetchMovieDetailStream(
          widget.slug,
          initialMovie: widget.initialMovie,
        ).listen(
          (movie) {
            if (mounted) {
              if (_movie == null) {
                // FirebaseApi.saveContinueWatching(movie, movie.currentEpisode);
              }
              setState(() {
                _movie = movie;
                _isLoading = false;
              });

              _categorizeServers(movie.episodes);

              if (_actors.isEmpty) {
                _fetchActors(movie);
              }

              _fetchTmdbRating(movie);

              // Bắt đầu timer phát trailer sau khi có dữ liệu đầu tiên
              if (_autoPlayTimer == null &&
                  !_trailerNotFound &&
                  !_showInlineTrailer &&
                  !_trailerEnded) {
                _autoPlayTimer = Timer(const Duration(seconds: 3), () {
                  _startInlineTrailer();
                });
              }
            }
          },
          onDone: () {
            if (mounted && _movie == null) {
              setState(() {
                _movie = widget.initialMovie;
                _isLoading = false;
              });
            }
          },
        );
  }

  Future<void> _fetchTmdbRating(Movie movie) async {
    try {
      final isTvSeries = movie.episodes.isNotEmpty && movie.episodes.first.items.length > 1;
      final rating = await PhimApi.getMovieTmdbRating(
        movie.name,
        movie.originalName,
        movie.year,
        isTvSeries,
      );
      if (mounted && rating != null && rating != '0.0') {
        setState(() {
          _tmdbRating = rating;
        });
      }

      // Luôn cố gắng lấy backdrop chất lượng cao từ TMDB để làm poster ngang
      final backdrop = await PhimApi.getMovieTmdbBackdrop(
        movie.name,
        movie.originalName,
        movie.year,
        isTvSeries,
      );
      if (mounted && backdrop != null && backdrop.isNotEmpty) {
        setState(() {
          _movie = movie.copyWith(posterUrl: backdrop);
        });
      }
    } catch (e) {
      print('Fetch TMDB rating/backdrop error: $e');
    }
  }

  Future<void> _fetchActors(Movie m) async {
    final actors = await PhimApi.getMovieActors(
      m.name,
      m.originalName,
      m.year,
      m.slug.contains('phim-bo'),
    );
    if (mounted && actors.isNotEmpty) {
      setState(() {
        _actors = actors;
      });
    }
  }

  void _categorizeServers(List<EpisodeServer> servers) {
    _premiumServers.clear();
    _tmServers.clear();
    _vietsubServers.clear();
    _p2pServers.clear();

    for (var server in servers) {
      final name = server.serverName.toLowerCase();
      if (name.contains('p2p') || name.contains('torrent')) {
        _p2pServers.add(server);
      } else if (name.contains('premium') ||
          name.contains('4k') ||
          name.contains('vip')) {
        _premiumServers.add(server);
      } else if (name.contains('thuyết minh') ||
          name.contains('lồng tiếng') ||
          name.contains('tm')) {
        _tmServers.add(server);
      } else {
        _vietsubServers.add(server);
      }
    }

    // Chỉ set default server nếu chưa có server nào được chọn
    // hoặc server đang chọn không còn tồn tại trong danh sách mới
    final currentStillExists = _currentServer != null &&
        servers.any((s) => s.serverName == _currentServer!.serverName);

    if (!currentStillExists) {
      if (_premiumServers.isNotEmpty) {
        _currentServer = _premiumServers.first;
      } else if (_vietsubServers.isNotEmpty) {
        _currentServer = _vietsubServers.first;
      } else if (_tmServers.isNotEmpty) {
        _currentServer = _tmServers.first;
      } else if (servers.isNotEmpty) {
        _currentServer = servers.first;
      }
    } else {
      // Cập nhật _currentServer sang object mới nhất (có thể episode list đã update)
      _currentServer = servers.firstWhere(
        (s) => s.serverName == _currentServer!.serverName,
        orElse: () => _currentServer!,
      );
    }
  }

  Future<void> _startInlineTrailer() async {
    if (_movie == null || !mounted) return;

    if (_isWebviewInitialized) {
      _webviewController.executeScript(
        "if(player && player.playVideo) { player.seekTo(0); player.playVideo(); }",
      );
      setState(() {
        _showInlineTrailer = true;
        _isTrailerPaused = false;
        _trailerEnded = false;
        _isTrailerExpanded = false;
      });
      return;
    }

    setState(() {
      _isLoadingTrailer = true;
    });

    final isTv =
        _movie!.slug.contains('phim-bo') ||
        _movie!.currentEpisode.toLowerCase().contains('tập');
    final ytKey = await PhimApi.getTrailerStreamUrl(
      _movie!.name,
      _movie!.originalName,
      _movie!.year,
      isTv,
    );

    if (ytKey != null && mounted) {
      await _initWebview(ytKey);
      if (mounted) {
        setState(() {
          _isLoadingTrailer = false;
          if (_autoPlayTrailerSetting) {
            _showInlineTrailer = true;
            _isTrailerPaused = false;
          } else {
            _showInlineTrailer = false;
            _isTrailerPaused = false; // Để UI hiện 'Phát Trailer' ban đầu
          }
          _trailerEnded = false;
          _isTrailerExpanded = false; // Luôn thu nhỏ khi mới bắt đầu
        });
      }
    } else {
      if (mounted) {
        setState(() {
          _trailerNotFound = true;
          _isLoadingTrailer = false;
        });
      }
    }
  }

  Future<void> _initWebview(String videoId) async {
    if (_isWebviewInitialized) return;

    _trailerServer = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    _trailerPort = _trailerServer!.port;

    _trailerServer!.listen((HttpRequest request) {
      if (request.uri.path == '/trailer.html') {
        final html =
            '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Trailer</title>
    <style>
      body, html { width: 100%; height: 100%; margin: 0; padding: 0; background-color: black; overflow: hidden; pointer-events: none; }
      #player { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; border: none; pointer-events: none; }
    </style>
  </head>
  <body>
    <div id="player"></div>
    <script>
      var tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '100%',
          width: '100%',
          videoId: '$videoId',
          playerVars: {
            'autoplay': ${_autoPlayTrailerSetting ? 1 : 0},
            'rel': 0,
            'modestbranding': 1,
            'fs': 0,
            'iv_load_policy': 3,
            'controls': 0,
            'disablekb': 1,
            'hl': 'vi',
            'cc_lang_pref': 'vi'
          },
          events: {
            'onReady': function(event) {
              event.target.setVolume(35);
              event.target.unMute();
              ${_autoPlayTrailerSetting ? 'event.target.playVideo();' : ''}
            },
            'onStateChange': function(event) {
              if (window.chrome && window.chrome.webview) {
                 window.chrome.webview.postMessage(event.data.toString());
              }
            }
          }
        });
      }
    </script>
  </body>
</html>
''';
        request.response
          ..headers.contentType = ContentType.html
          ..write(html)
          ..close();
      } else {
        request.response.statusCode = HttpStatus.notFound;
        request.response.close();
      }
    });

    try {
      await _webviewController.initialize();
      await _webviewController.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      );

      _webviewController.webMessage.listen((msg) {
        if (msg == '0') {
          // 0 = ended
          if (mounted) {
            setState(() {
              _showInlineTrailer = false;
              _isTrailerPaused = false;
              _trailerEnded = true;
              _isTrailerExpanded = false;
            });
          }
        }
      });

      final url = 'http://127.0.0.1:$_trailerPort/trailer.html';
      await _webviewController.loadUrl(url);

      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }
    } catch (e) {
      print('Inline Webview Error: $e');
    }
  }

  void _toggleExpandTrailer() {
    if (!_showInlineTrailer || _trailerEnded) return;
    setState(() {
      _isTrailerExpanded = !_isTrailerExpanded;
    });
    if (_isTrailerExpanded) {
      _webviewController.executeScript(
        "if(player && player.unMute) { player.unMute(); player.setVolume(100); }",
      );
    } else {
      _webviewController.executeScript(
        "if(player && player.setVolume) { player.setVolume(35); }",
      );
    }
  }

  Widget _buildMainTab(String id, String label, IconData icon) {
    final isActive = _activeMainTab == id;
    return GestureDetector(
      onTap: () {
        setState(() {
          _activeMainTab = id;
          if (id == 'Promax') {
            if (_premiumServers.isNotEmpty)
              _currentServer = _premiumServers.first;
            else if (_p2pServers.isNotEmpty)
              _currentServer = _p2pServers.first;
            else
              _currentServer = null;
          } else {
            if (_activeStandardSubTab == 'Vietsub' &&
                _vietsubServers.isNotEmpty)
              _currentServer = _vietsubServers.first;
            else if (_tmServers.isNotEmpty)
              _currentServer = _tmServers.first;
            else if (_vietsubServers.isNotEmpty)
              _currentServer = _vietsubServers.first;
            else
              _currentServer = null;
          }
          _selectedSeason = null;
          _selectedP2pEpisode = null;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        decoration: BoxDecoration(
          color: isActive
              ? Colors.redAccent.withOpacity(0.2)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isActive ? Colors.redAccent : Colors.white.withOpacity(0.1),
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isActive ? Colors.redAccent : Colors.white54,
              size: 20,
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                color: isActive ? Colors.white : Colors.white54,
                fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSubTab(String id, String label) {
    final isActive = _activeStandardSubTab == id;
    return GestureDetector(
      onTap: () {
        setState(() {
          _activeStandardSubTab = id;
          if (id == 'Vietsub' && _vietsubServers.isNotEmpty)
            _currentServer = _vietsubServers.first;
          else if (id == 'Thuyết Minh' && _tmServers.isNotEmpty)
            _currentServer = _tmServers.first;
          else
            _currentServer = null;
        });
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          border: Border(
            bottom: BorderSide(
              color: isActive ? Colors.blueAccent : Colors.transparent,
              width: 2,
            ),
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isActive ? Colors.white : Colors.white54,
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ),
    );
  }

  Widget _buildEpisodesGrid() {
    if (_currentServer == null) return const SizedBox();

    final serverNameLower = _currentServer!.serverName.toLowerCase();
    final isP2p = serverNameLower.contains('p2p') ||
        serverNameLower.contains('torrent');
    // Embed servers (VidSrc, VidAPI) dùng slug S1E1 nhưng không phải P2P,
    // chúng cần được hiển thị dạng season nhưng mở trực tiếp qua PlayerScreen
    final isEmbedServer = serverNameLower.contains('vidsrc') ||
        serverNameLower.contains('vidapi') ||
        serverNameLower.contains('embed');

    // Chỉ kích hoạt season UI khi server là P2P hoặc Embed có slug S1E1
    bool hasSeasons = false;
    if ((isP2p || isEmbedServer) && _currentServer!.items.isNotEmpty) {
      final firstSlug = _currentServer!.items.first.slug;
      if (firstSlug.isNotEmpty && RegExp(r'S(\d+)E(\d+)').hasMatch(firstSlug)) {
        hasSeasons = true;
      }
    }

    if (!hasSeasons) {
      // Normal flat list rendering
      return Wrap(
        spacing: 12,
        runSpacing: 12,
        children: _currentServer!.items.asMap().entries.map((entry) {
          final index = entry.key;
          final ep = entry.value;
          return HoverEpisodeButton(
            text: ep.name,
            onTap: () async {
              _pauseTrailer();
              FirebaseApi.saveContinueWatching(_movie!, ep.name);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => PlayerScreen(
                    episodes: _currentServer!.items,
                    currentEpisodeIndex: index,
                    movieName: _movie!.name,
                    imdbId: _movie!.imdbId,
                  ),
                ),
              );
            },
          );
        }).toList(),
      );
    }

    // P2P TV Series UI: Season -> Episode -> Streams
    // 1. Group items by Season
    final Map<int, List<Episode>> seasonsMap = {};
    for (var ep in _currentServer!.items) {
      // Extract season from slug 'S1E1'
      final match = RegExp(r'S(\d+)E(\d+)').firstMatch(ep.slug);
      if (match != null) {
        final s = int.parse(match.group(1)!);
        seasonsMap.putIfAbsent(s, () => []).add(ep);
      }
    }
    final seasons = seasonsMap.keys.toList()..sort();

    if (_selectedSeason == null && seasons.isNotEmpty) {
      _selectedSeason = seasons.first;
      // Try to parse season from movie name (e.g., 'Phần 3', 'Season 3')
      final match = RegExp(r'(?:season|phần|part)\s*(\d+)', caseSensitive: false).firstMatch(_movie!.name);
      if (match != null) {
        final s = int.tryParse(match.group(1)!);
        if (s != null && seasons.contains(s)) {
          _selectedSeason = s;
        }
      }
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Seasons Selector
        Text(L10n.t('select_season') + ':', style: const TextStyle(color: Colors.white70)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: seasons.map((s) {
            final isActive = _selectedSeason == s;
            return GestureDetector(
              onTap: () => setState(() {
                _selectedSeason = s;
                _selectedP2pEpisode = null;
              }),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                decoration: BoxDecoration(
                  color: isActive
                      ? Colors.redAccent
                      : Colors.white.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  'Mùa $s',
                  style: TextStyle(
                    color: isActive ? Colors.white : Colors.white70,
                  ),
                ),
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 24),

        // Episodes Selector
        if (_selectedSeason != null) ...[
          Text(L10n.t('select_episode') + ':', style: const TextStyle(color: Colors.white70)),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: seasonsMap[_selectedSeason!]!.map((ep) {
              final isActive = _selectedP2pEpisode == ep;
              return GestureDetector(
                onTap: () async {
                  if (isP2p) {
                    // Chỉ P2P/Torrent mới cần fetch streams riêng
                    _fetchP2pStreamsForEpisode(ep);
                  } else {
                    // Embed servers (VidSrc, VidAPI) và các server thường
                    // đều mở thẳng PlayerScreen với index đúng trong danh sách
                    _pauseTrailer();
                    FirebaseApi.saveContinueWatching(_movie!, ep.name);
                    final index = _currentServer!.items.indexOf(ep);
                    final seasonEpMatch = RegExp(r'S(\d+)E(\d+)').firstMatch(ep.slug);
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: _currentServer!.items,
                          currentEpisodeIndex: index,
                          movieName: _movie!.name,
                          imdbId: _movie!.imdbId,
                          season: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(1)!) : null,
                          episode: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(2)!) : null,
                        ),
                      ),
                    );
                  }
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: isActive
                        ? Colors.blueAccent
                        : Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    ep.name,
                    style: TextStyle(
                      color: isActive ? Colors.white : Colors.white70,
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 24),
        ],

        // Streams Display
        if (_selectedP2pEpisode != null) ...[
          Text(
            'Chọn Luồng phát (Chất lượng):',
            style: TextStyle(color: Colors.white70),
          ),
          const SizedBox(height: 8),
          if (_isFetchingP2pStreams)
            const Padding(
              padding: EdgeInsets.all(16),
              child: CircularProgressIndicator(),
            )
          else if (_p2pStreams.isEmpty)
            Text(L10n.t('no_streams_found'),
              style: TextStyle(color: Colors.redAccent),
            )
          else
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _p2pStreams.asMap().entries.map((entry) {
                final idx = entry.key;
                final stream = entry.value;
                return HoverEpisodeButton(
                  text: stream.name,
                  onTap: () async {
                    _pauseTrailer();
                    FirebaseApi.saveContinueWatching(
                      _movie!,
                      '${_selectedP2pEpisode!.slug} - ${stream.name}',
                    );
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: _p2pStreams,
                          currentEpisodeIndex: idx,
                          movieName:
                              '${_movie!.displayName} - ${_selectedP2pEpisode!.slug}',
                        ),
                      ),
                    );
                  },
                );
              }).toList(),
            ),
        ],
      ],
    );
  }

  Future<void> _fetchP2pStreamsForEpisode(Episode ep) async {
    setState(() {
      _selectedP2pEpisode = ep;
      _isFetchingP2pStreams = true;
      _p2pStreams = [];
    });

    try {
      // m3u8Url format: torrentio://imdbId:season:episode
      final parts = ep.m3u8Url.replaceAll('torrentio://', '').split(':');
      if (parts.length == 3) {
        final imdbId = parts[0];
        final season = int.parse(parts[1]);
        final episode = int.parse(parts[2]);

        final servers = await TorrentioApi.fetchStreams(
          imdbId,
          season: season,
          episode: episode,
        );
        if (servers.isNotEmpty && mounted) {
          setState(() {
            _p2pStreams = servers.first.items;
          });
        }
      }
    } catch (e) {
      print('Fetch P2P stream error: $e');
    } finally {
      if (mounted) {
        setState(() {
          _isFetchingP2pStreams = false;
        });
      }
    }
  }

  Widget _buildServerTab(
    EpisodeServer server, {
    bool isPremium = false,
    bool isMotchillGroup = false,
    bool isSubServer = false,
    List<EpisodeServer> motchillGroup = const [],
  }) {
    bool isSelected = _currentServer == server;
    if (isMotchillGroup) {
      isSelected =
          _currentServer != null &&
          _currentServer!.serverName.toLowerCase().startsWith('motchill');
    }

    String displayName = server.serverName;
    if (isMotchillGroup) {
      displayName = 'Motchill Server';
    } else if (isSubServer) {
      displayName = displayName
          .replaceFirst(RegExp(r'^Motchill\s*'), '')
          .trim();
    } else if (!isPremium) {
      displayName = displayName
          .replaceAll(
            RegExp(
              r'\s*-\s*(vietsub|thuyết minh|lồng tiếng|tm|thuyet minh)',
              caseSensitive: false,
            ),
            '',
          )
          .trim();
    }

    return HoverServerTab(
      text: displayName,
      isPremium: isPremium,
      isSelected: isSelected,
      onTap: () {
        setState(() {
          if (isMotchillGroup) {
            if (!isSelected && motchillGroup.isNotEmpty) {
              _currentServer = motchillGroup.first;
            }
          } else {
            _currentServer = server;
          }
        });
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        backgroundColor: const Color(0xFF111111),
        appBar: AppBar(
          backgroundColor: Colors.black,
          centerTitle: false,
          titleSpacing: 0,
          title: Image.asset('assets/logo.png', height: 24),
        ),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_movie == null) {
      return Scaffold(
        backgroundColor: const Color(0xFF111111),
        appBar: AppBar(
          backgroundColor: Colors.black,
          centerTitle: false,
          titleSpacing: 0,
          title: Image.asset('assets/logo.png', height: 24),
        ),
        body: Center(
          child: Text(
            'Không tìm thấy thông tin phim.',
            style: TextStyle(color: Colors.white),
          ),
        ),
      );
    }

    final bool hasBackdrop =
        _movie!.posterUrl.isNotEmpty && _movie!.posterUrl != _movie!.thumbUrl;
    final String heroImage = hasBackdrop ? _movie!.posterUrl : _movie!.thumbUrl;
    final double fullHeight = MediaQuery.of(context).size.width * 9 / 16;
    final double collapsedHeight = fullHeight > 450.0 ? 450.0 : fullHeight;
    final double currentBannerHeight = _isTrailerExpanded
        ? fullHeight
        : collapsedHeight;

    final bool isSeries =
        _movie!.episodes.isNotEmpty && _movie!.episodes.first.items.length > 1;
    final String episodeText = isSeries
        ? '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}'
        : _movie!.currentEpisode;

    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      body: Stack(
        children: [
          // 0. Ambient Blurred Background (Apple style)
          Positioned.fill(
            child: CachedNetworkImage(
              imageUrl: _movie!.thumbUrl,
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 80.0, sigmaY: 80.0),
              child: Container(
                color: Colors.black.withOpacity(0.6), // Phủ đen nhẹ lên màu gốc
              ),
            ),
          ),

          // 1. Background Media (Banner / Trailer)
          AnimatedPositioned(
            duration: const Duration(milliseconds: 400),
            curve: Curves.easeInOut,
            top: 0,
            left: 0,
            right: 0,
            height: currentBannerHeight,
            child: Stack(
              children: [
                Positioned.fill(
                  child: _showInlineTrailer && _isWebviewInitialized
                      ? Webview(_webviewController)
                      : (hasBackdrop
                            ? Hero(
                                tag: widget.heroTag ?? widget.slug,
                                child: CachedNetworkImage(
                                  imageUrl: heroImage,
                                  fit: BoxFit.cover,
                                  alignment: Alignment.topCenter,
                                ),
                              )
                            : const SizedBox.shrink()),
                ),
              ],
            ),
          ),

          // 2. Full-screen touch overlay for expanding/shrinking Trailer
          if (_showInlineTrailer && !_trailerEnded)
            Positioned.fill(
              child: GestureDetector(
                onTap: _toggleExpandTrailer,
                child: Container(color: Colors.transparent),
              ),
            ),

          // 3. Main Foreground (Scrollable Content + Overlays)
          Positioned.fill(
            child: IgnorePointer(
              ignoring:
                  _isTrailerExpanded, // Khi mở rộng trailer thì không chặn tương tác
              child: AnimatedOpacity(
                duration: const Duration(milliseconds: 400),
                opacity: _isTrailerExpanded ? 0.0 : 1.0,
                child: CustomScrollView(
                  slivers: [
                    // Khoảng trống để lộ phần Video bên trên
                    SliverToBoxAdapter(
                      child: GestureDetector(
                        behavior: HitTestBehavior.translucent,
                        onTap: _showInlineTrailer && !_trailerEnded
                            ? _toggleExpandTrailer
                            : null,
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 400),
                          curve: Curves.easeInOut,
                          height: _isTrailerExpanded
                              ? fullHeight
                              : (collapsedHeight > 400
                                    ? collapsedHeight - 200
                                    : 200),
                        ),
                      ),
                    ),

                    // Phần Content đè lên dưới của Video
                    SliverToBoxAdapter(
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Colors.black.withOpacity(0.0),
                              Colors.black.withOpacity(0.8),
                              Colors.black,
                            ],
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                            stops: const [0.0, 0.15, 1.0],
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(40, 20, 40, 40),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // Hàng 1: Thông tin chính
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.end,
                                children: [
                                  if (!hasBackdrop) ...[
                                    ClipRRect(
                                      borderRadius: BorderRadius.circular(12),
                                      child: Hero(
                                        tag: widget.heroTag ?? widget.slug,
                                        child: CachedNetworkImage(
                                          imageUrl: _movie!.thumbUrl,
                                          width: 160,
                                          height: 240,
                                          fit: BoxFit.cover,
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 32),
                                  ],
                                  // Text Info
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      mainAxisAlignment: MainAxisAlignment.end,
                                      children: [
                                        Text(
                                          _movie!.displayName,
                                          style: const TextStyle(
                                            fontSize: 48,
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                            height: 1.1,
                                            shadows: [
                                              Shadow(
                                                color: Colors.black,
                                                blurRadius: 10,
                                              ),
                                            ],
                                          ),
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          _movie!.originalName,
                                          style: TextStyle(
                                            fontSize: 20,
                                            color: Colors.white.withOpacity(
                                              0.7,
                                            ),
                                            shadows: const [
                                              Shadow(
                                                color: Colors.black,
                                                blurRadius: 5,
                                              ),
                                            ],
                                          ),
                                        ),
                                        const SizedBox(height: 16),

                                        // Badges
                                        Wrap(
                                          spacing: 12,
                                          runSpacing: 8,
                                          crossAxisAlignment:
                                              WrapCrossAlignment.center,
                                          children: [
                                            if (_tmdbRating != null)
                                              _buildBadgeIcon(
                                                Icons.star,
                                                'IMDb: $_tmdbRating',
                                                color: Colors.amber,
                                              ),
                                            if (_premiumServers.isNotEmpty)
                                              _buildBadge(
                                                'Premium TM - Vietsub',
                                                Colors.blueAccent,
                                              ),
                                            _buildBadgeIcon(
                                              Icons.layers,
                                              episodeText,
                                            ),
                                            _buildBadgeIcon(
                                              Icons.timer,
                                              _movie!.time,
                                            ),
                                            _buildBadgeIcon(
                                              Icons.calendar_today,
                                              _movie!.year,
                                            ),
                                            if (_movie!.countries.isNotEmpty)
                                              _buildBadgeIcon(
                                                Icons.public,
                                                _movie!.countries.first,
                                              ),
                                          ],
                                        ),
                                        const SizedBox(height: 16),
                                        _buildRatingSection(),
                                        const SizedBox(height: 24),

                                        // Share & Trailer Buttons
                                        Row(
                                          children: [
                                            ElevatedButton.icon(
                                              onPressed: () {
                                                final shareUrl =
                                                    'https://mytv4u.web.app/share/${_movie!.slug}?source=${_movie!.source}';
                                                Clipboard.setData(
                                                  ClipboardData(text: shareUrl),
                                                );
                                                UIUtils.showCustomSnackBar(
                                                  context,
                                                  '🎟️ Đã copy link Xem Phim: $shareUrl',
                                                );
                                              },
                                              icon: const Icon(
                                                Icons.share,
                                                color: Colors.black,
                                                size: 20,
                                              ),
                                              label: Text(
                                                L10n.t('share'),
                                                style: const TextStyle(
                                                  color: Colors.black,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor: const Color(
                                                  0xFFF59E0B,
                                                ),
                                                padding:
                                                    const EdgeInsets.symmetric(
                                                      vertical: 14,
                                                      horizontal: 20,
                                                    ),
                                                shape: RoundedRectangleBorder(
                                                  borderRadius:
                                                      BorderRadius.circular(12),
                                                ),
                                              ),
                                            ),
                                            const SizedBox(width: 12),
                                            ElevatedButton.icon(
                                              onPressed: _toggleWatchlist,
                                              icon: Icon(
                                                _isInWatchlist
                                                    ? Icons.favorite
                                                    : Icons.favorite_border,
                                                color: _isInWatchlist
                                                    ? Colors.redAccent
                                                    : Colors.white,
                                                size: 20,
                                              ),
                                              label: Text(
                                                L10n.t('favorite'),
                                                style: TextStyle(
                                                  color: _isInWatchlist
                                                      ? Colors.redAccent
                                                      : Colors.white,
                                                ),
                                              ),
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor: Colors.white
                                                    .withOpacity(0.15),
                                                padding:
                                                    const EdgeInsets.symmetric(
                                                      vertical: 14,
                                                      horizontal: 20,
                                                    ),
                                                shape: RoundedRectangleBorder(
                                                  borderRadius:
                                                      BorderRadius.circular(12),
                                                ),
                                              ),
                                            ),
                                            const SizedBox(width: 12),
                                            if (_trailerNotFound)
                                              ElevatedButton.icon(
                                                onPressed: () {
                                                  final url = Uri.parse(
                                                    'https://www.youtube.com/results?search_query=${Uri.encodeComponent("${_movie!.displayName} trailer")}',
                                                  );
                                                  launchUrl(url);
                                                },
                                                icon: const Icon(
                                                  Icons.search,
                                                  color: Colors.white,
                                                ),
                                                label: Text(
                                                  L10n.t('trailer_search'),
                                                  style: const TextStyle(color: Colors.white),
                                                ),
                                                style: ElevatedButton.styleFrom(
                                                  backgroundColor: Colors.white.withOpacity(0.15),
                                                  padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                                                  shape: RoundedRectangleBorder(
                                                    borderRadius: BorderRadius.circular(12),
                                                  ),
                                                ),
                                              )
                                            else if (_isLoadingTrailer)
                                              ElevatedButton.icon(
                                                onPressed: null,
                                                icon: const SizedBox(
                                                  width: 20,
                                                  height: 20,
                                                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                                                ),
                                                label: Text(L10n.t('loading'),
                                                  style: TextStyle(color: Colors.white),
                                                ),
                                                style: ElevatedButton.styleFrom(
                                                  backgroundColor: Colors.white.withOpacity(0.15),
                                                  padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                                                  shape: RoundedRectangleBorder(
                                                    borderRadius: BorderRadius.circular(12),
                                                  ),
                                                ),
                                              )
                                            else if (_isWebviewInitialized)
                                              if (_showInlineTrailer)
                                                ElevatedButton.icon(
                                                  onPressed: _pauseTrailer,
                                                  icon: const Icon(
                                                    Icons.stop,
                                                    color: Colors.white,
                                                  ),
                                                  label: Text(L10n.t('trailer_stop'),
                                                    style: TextStyle(color: Colors.white),
                                                  ),
                                                  style: ElevatedButton.styleFrom(
                                                    backgroundColor: Colors.redAccent.withOpacity(0.8),
                                                    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                                                    shape: RoundedRectangleBorder(
                                                      borderRadius: BorderRadius.circular(12),
                                                    ),
                                                  ),
                                                )
                                              else if (_trailerEnded)
                                                ElevatedButton.icon(
                                                  onPressed: _playTrailer,
                                                  icon: const Icon(
                                                    Icons.replay,
                                                    color: Colors.white,
                                                  ),
                                                  label: Text(L10n.t('trailer_replay'),
                                                    style: TextStyle(color: Colors.white),
                                                  ),
                                                  style: ElevatedButton.styleFrom(
                                                    backgroundColor: Colors.white.withOpacity(0.15),
                                                    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                                                    shape: RoundedRectangleBorder(
                                                      borderRadius: BorderRadius.circular(12),
                                                    ),
                                                  ),
                                                )
                                              else
                                                ElevatedButton.icon(
                                                  onPressed: _isTrailerPaused ? _resumeTrailer : _playTrailer,
                                                  icon: const Icon(
                                                    Icons.play_arrow,
                                                    color: Colors.white,
                                                  ),
                                                  label: Text(
                                                    _isTrailerPaused ? L10n.t('trailer_resume') : L10n.t('trailer_play'),
                                                    style: const TextStyle(color: Colors.white),
                                                  ),
                                                  style: ElevatedButton.styleFrom(
                                                    backgroundColor: Colors.white.withOpacity(0.15),
                                                    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                                                    shape: RoundedRectangleBorder(
                                                      borderRadius: BorderRadius.circular(12),
                                                    ),
                                                  ),
                                                )
                                            ],
                                          ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),

                              const SizedBox(height: 40),

                              // Poster & Details
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Poster
                                  HoverPoster(movie: _movie!),
                                  const SizedBox(width: 24),
                                  Expanded(
                                    flex: 2,
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        if (_movie!.genres.isNotEmpty) ...[
                                          _buildRichText(
                                            L10n.t('genres'),
                                            _movie!.genres.join(', '),
                                          ),
                                          const SizedBox(height: 8),
                                        ],
                                        if (_movie!.directors.isNotEmpty &&
                                            _movie!.directors
                                                .join()
                                                .trim()
                                                .isNotEmpty) ...[
                                          _buildRichText(
                                            L10n.t('directors'),
                                            _movie!.directors.join(', '),
                                          ),
                                          const SizedBox(height: 8),
                                        ],
                                        const SizedBox(height: 16),
                                        Text(
                                          _movie!.description.replaceAll(
                                            RegExp(r'<[^>]*>|&[^;]+;'),
                                            '',
                                          ),
                                          style: TextStyle(
                                            fontSize: 15,
                                            color: Colors.white.withOpacity(
                                              0.8,
                                            ),
                                            height: 1.6,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(width: 40),

                                  // Cột Diễn viên (Nếu có)
                                  if (_actors.isNotEmpty)
                                    Expanded(
                                      flex: 1,
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            L10n.t('actors'),
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                              fontSize: 16,
                                            ),
                                          ),
                                          const SizedBox(height: 16),
                                          Wrap(
                                            spacing: 16,
                                            runSpacing: 16,
                                            children: _actors.take(6).map((
                                              actor,
                                            ) {
                                              return MouseRegion(
                                                cursor:
                                                    SystemMouseCursors.click,
                                                child: GestureDetector(
                                                  onTap: () async {
                                                    if (actor['id'] != null &&
                                                        actor['id']!.isNotEmpty) {
                                                      _pauseTrailer();
                                                      Navigator.push(
                                                        context,
                                                        MaterialPageRoute(
                                                          builder: (_) =>
                                                              ActorDetailScreen(
                                                                actorId:
                                                                    actor['id']!,
                                                                actorName:
                                                                    actor['name'] ??
                                                                    '',
                                                              ),
                                                        ),
                                                      );
                                                    }
                                                  },
                                                  child: Column(
                                                    children: [
                                                      Container(
                                                        width: 60,
                                                        height: 60,
                                                        decoration:
                                                            BoxDecoration(
                                                              shape: BoxShape
                                                                  .circle,
                                                              border: Border.all(
                                                                color: Colors
                                                                    .white24,
                                                              ),
                                                              color: Colors
                                                                  .white
                                                                  .withOpacity(
                                                                    0.05,
                                                                  ),
                                                            ),
                                                        child: ClipOval(
                                                          child:
                                                              (actor['profile'] !=
                                                                      null &&
                                                                  actor['profile']!
                                                                      .isNotEmpty)
                                                              ? CachedNetworkImage(
                                                                  imageUrl:
                                                                      actor['profile']!,
                                                                  fit: BoxFit
                                                                      .cover,
                                                                  errorWidget:
                                                                      (
                                                                        context,
                                                                        url,
                                                                        error,
                                                                      ) => const Icon(
                                                                        Icons
                                                                            .person,
                                                                        color: Colors
                                                                            .white38,
                                                                        size:
                                                                            30,
                                                                      ),
                                                                )
                                                              : const Icon(
                                                                  Icons.person,
                                                                  color: Colors
                                                                      .white38,
                                                                  size: 30,
                                                                ),
                                                        ),
                                                      ),
                                                      const SizedBox(height: 6),
                                                      SizedBox(
                                                        width: 70,
                                                        child: Text(
                                                          actor['name'] ?? '',
                                                          style:
                                                              const TextStyle(
                                                                color: Colors
                                                                    .white,
                                                                fontSize: 11,
                                                              ),
                                                          textAlign:
                                                              TextAlign.center,
                                                          maxLines: 2,
                                                          overflow: TextOverflow
                                                              .ellipsis,
                                                        ),
                                                      ),
                                                    ],
                                                  ),
                                                ),
                                              );
                                            }).toList(),
                                          ),
                                        ],
                                      ),
                                    ),
                                ],
                              ),

                              const SizedBox(height: 60),

                              // Servers and Episodes
                              if (_movie!.episodes.isEmpty) ...[
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    vertical: 24,
                                    horizontal: 24,
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.white.withOpacity(0.05),
                                    borderRadius: BorderRadius.circular(12),
                                    border: Border.all(
                                      color: Colors.white.withOpacity(0.1),
                                    ),
                                  ),
                                  child: Row(
                                    children: [
                                      const Icon(
                                        Icons.info_outline,
                                        color: Colors.blueAccent,
                                        size: 28,
                                      ),
                                      const SizedBox(width: 16),
                                      Expanded(
                                        child: Text(
                                          L10n.t('movie_not_released'),
                                          style: const TextStyle(
                                            color: Colors.white70,
                                            fontSize: 16,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ] else ...[
                                Text(L10n.t('select_episode').toUpperCase(),
                                  style: TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                                const SizedBox(height: 24),

                                // --- TABS CHÍNH ---
                                Row(
                                  children: [
                                    _buildMainTab(
                                      'Promax',
                                      L10n.t('source_promax'),
                                      Icons.stars,
                                    ),
                                    const SizedBox(width: 16),
                                    _buildMainTab(
                                      'Standard',
                                      L10n.t('source_standard'),
                                      Icons.list,
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 24),

                                // --- NỘI DUNG THEO TAB CHÍNH ---
                                if (_activeMainTab == 'Promax') ...[
                                  // Hiển thị các nút chọn nguồn Promax (Premium, P2P)
                                  Builder(
                                    builder: (context) {
                                      final promaxServers = [
                                        ..._premiumServers,
                                        ..._p2pServers,
                                      ];
                                      if (promaxServers.isEmpty)
                                        return Text(
                                          L10n.t('no_promax_source'),
                                          style: const TextStyle(
                                            color: Colors.white54,
                                          ),
                                        );
                                      return Wrap(
                                        spacing: 12,
                                        runSpacing: 12,
                                        children: promaxServers
                                            .map(
                                              (s) => _buildServerTab(
                                                s,
                                                isPremium: s.serverName
                                                    .toLowerCase()
                                                    .contains('premium'),
                                              ),
                                            )
                                            .toList(),
                                      );
                                    },
                                  ),
                                ] else if (_activeMainTab == 'Standard') ...[
                                  // Sub-tabs: Thuyết minh / Phụ đề
                                  Row(
                                    children: [
                                      _buildSubTab('Vietsub', 'Phụ đề'),
                                      const SizedBox(width: 12),
                                      _buildSubTab(
                                        'Thuyết Minh',
                                        'Thuyết minh / Lồng tiếng',
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 16),

                                  // Hiển thị các nguồn Standard dựa theo Sub-tab
                                  Builder(
                                    builder: (context) {
                                      final targetServers =
                                          _activeStandardSubTab == 'Vietsub'
                                          ? _vietsubServers
                                          : _tmServers;
                                      if (targetServers.isEmpty)
                                        return Text(
                                          'Không có nguồn nào trong mục này.',
                                          style: TextStyle(
                                            color: Colors.white54,
                                          ),
                                        );

                                      final List<EpisodeServer> displayServers =
                                          [];
                                      final motchillGroup = targetServers
                                          .where(
                                            (s) => s.serverName
                                                .toLowerCase()
                                                .startsWith('motchill'),
                                          )
                                          .toList();
                                      for (var s in targetServers) {
                                        if (s.serverName
                                            .toLowerCase()
                                            .startsWith('motchill')) {
                                          if (!displayServers.any(
                                            (x) =>
                                                x.serverName ==
                                                'Motchill Server',
                                          )) {
                                            displayServers.add(
                                              EpisodeServer(
                                                serverName: 'Motchill Server',
                                                items: [],
                                              ),
                                            ); // Dummy
                                          }
                                        } else {
                                          displayServers.add(s);
                                        }
                                      }

                                      return Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Wrap(
                                            spacing: 12,
                                            runSpacing: 12,
                                            children: displayServers.map((s) {
                                              if (s.serverName ==
                                                  'Motchill Server') {
                                                return _buildServerTab(
                                                  s,
                                                  isPremium: false,
                                                  isMotchillGroup: true,
                                                  motchillGroup: motchillGroup,
                                                );
                                              }
                                              return _buildServerTab(
                                                s,
                                                isPremium: false,
                                              );
                                            }).toList(),
                                          ),
                                          if (_currentServer != null &&
                                              _currentServer!.serverName
                                                  .toLowerCase()
                                                  .startsWith('motchill') &&
                                              motchillGroup.isNotEmpty) ...[
                                            const SizedBox(height: 12),
                                            Container(
                                              padding: const EdgeInsets.only(
                                                left: 16,
                                              ),
                                              decoration: BoxDecoration(
                                                border: Border(
                                                  left: BorderSide(
                                                    color: Colors.white
                                                        .withOpacity(0.1),
                                                    width: 2,
                                                  ),
                                                ),
                                              ),
                                              child: Wrap(
                                                spacing: 8,
                                                runSpacing: 8,
                                                children: motchillGroup
                                                    .map(
                                                      (s) => _buildServerTab(
                                                        s,
                                                        isPremium: false,
                                                        isSubServer: true,
                                                      ),
                                                    )
                                                    .toList(),
                                              ),
                                            ),
                                          ],
                                        ],
                                      );
                                    },
                                  ),
                                ],

                                const SizedBox(height: 32),

                                // --- DANH SÁCH TẬP PHIM / LUỒNG PHÁT ---
                                if (_currentServer != null) ...[
                                  Container(
                                    padding: const EdgeInsets.all(24),
                                    decoration: BoxDecoration(
                                      color: Colors.white.withOpacity(0.03),
                                      borderRadius: BorderRadius.circular(16),
                                      border: Border.all(
                                        color: Colors.white.withOpacity(0.05),
                                      ),
                                    ),
                                    child: _buildEpisodesGrid(),
                                  ),
                                ],
                              ],
                              _buildCommentsSection(),

                              const SizedBox(height: 100), // Đệm dưới cùng
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // Custom Window Controls (Title Bar)
          if (!_isTrailerExpanded)
            const Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: CustomTitleBar(),
            ),

          // Back Button
          if (!_isTrailerExpanded)
            Positioned(
              top: 48, // Cách xa mép trên
              left: 24, // Cách xa mép trái
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.3),
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  icon: const Icon(
                    Icons.arrow_back,
                    color: Colors.white,
                    size: 24,
                  ),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildBadge(String text, Color color) {
    return GlassContainer(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      borderRadius: 20,
      color: color.withOpacity(0.2),
      borderColor: color.withOpacity(0.5),
      child: Text(
        text,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.bold,
          fontSize: 12,
        ),
      ),
    );
  }

  Widget _buildRatingSection() {
    return Row(
      children: [
        Text(
          L10n.t('rating'),
          style: const TextStyle(color: Colors.white70, fontSize: 16),
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(5, (index) {
            final starIndex = index + 1;
            return MouseRegion(
              onEnter: (_) => setState(() => _hoverRating = starIndex),
              onExit: (_) => setState(() => _hoverRating = 0),
              cursor: SystemMouseCursors.click,
              child: GestureDetector(
                onTap: () async {
                  if (_isSubmittingRating) return;
                  setState(() => _isSubmittingRating = true);
                  final success = await FirebaseApi.submitRating(
                    widget.slug,
                    starIndex,
                  );
                  if (success) {
                    setState(() {
                      _userRating = starIndex;
                    });
                    await _fetchFirebaseRatings();
                  }
                  setState(() => _isSubmittingRating = false);
                },
                child: Icon(
                  Icons.star,
                  size: 28,
                  color:
                      (_hoverRating > 0
                          ? _hoverRating >= starIndex
                          : _userRating >= starIndex)
                      ? Colors.amber
                      : Colors.white24,
                ),
              ),
            );
          }),
        ),
        const SizedBox(width: 12),
        if (_isSubmittingRating)
          const SizedBox(
            width: 16,
            height: 16,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              color: Colors.amber,
            ),
          )
        else if (_totalRatings > 0)
          Text(
            '${_averageRating.toStringAsFixed(1)}/5 ($_totalRatings lượt)',
            style: const TextStyle(
              color: Colors.amber,
              fontWeight: FontWeight.bold,
              fontSize: 16,
            ),
          )
        else
          Text(
            L10n.t('no_rating'),
            style: const TextStyle(color: Colors.white54, fontSize: 14),
          ),
      ],
    );
  }

  Widget _buildBadgeIcon(IconData icon, String text, {Color? color}) {
    if (text.isEmpty) return const SizedBox.shrink();
    return GlassContainer(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      borderRadius: 20,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: color ?? Colors.white70),
          const SizedBox(width: 6),
          Text(
            text,
            style: TextStyle(color: color ?? Colors.white, fontSize: 12),
          ),
        ],
      ),
    );
  }

  Widget _buildRichText(String label, String value) {
    return RichText(
      text: TextSpan(
        children: [
          TextSpan(
            text: label,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 15,
            ),
          ),
          TextSpan(
            text: value,
            style: TextStyle(
              color: Colors.white.withOpacity(0.8),
              fontSize: 15,
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _handlePostComment() async {
    if (_commentController.text.trim().isEmpty) return;

    if (_currentUser == null) {
      final user = await AuthApi.loginWithGoogle();
      if (user != null) {
        setState(() => _currentUser = user);
        await _submitComment();
      }
    } else {
      await _submitComment();
    }
  }

  Future<void> _submitComment() async {
    if (_currentUser == null ||
        _commentController.text.trim().isEmpty ||
        _isSubmittingComment)
      return;

    setState(() => _isSubmittingComment = true);

    final newComment = await CommentApi.postComment(
      movieSlug: widget.slug,
      userId: _currentUser!['uid']!,
      userDisplayName: _currentUser!['displayName']!,
      userPhoto: _currentUser!['photoURL']!,
      text: _commentController.text,
    );

    if (newComment != null && mounted) {
      setState(() {
        _comments.insert(0, newComment);
        _commentController.clear();
      });
    }

    if (mounted) {
      setState(() => _isSubmittingComment = false);
    }
  }

  Future<void> _handlePostReply(String parentId) async {
    if (_replyController.text.trim().isEmpty) return;

    if (_currentUser == null) {
      final user = await AuthApi.loginWithGoogle();
      if (user != null) {
        setState(() => _currentUser = user);
        await _submitReply(parentId);
      }
    } else {
      await _submitReply(parentId);
    }
  }

  Future<void> _submitReply(String parentId) async {
    if (_currentUser == null ||
        _replyController.text.trim().isEmpty ||
        _isSubmittingReply)
      return;

    setState(() => _isSubmittingReply = true);

    final newReply = await CommentApi.replyToComment(
      parentId: parentId,
      userId: _currentUser!['uid']!,
      userDisplayName: _currentUser!['displayName']!,
      userPhoto: _currentUser!['photoURL']!,
      text: _replyController.text,
    );

    if (newReply != null && mounted) {
      setState(() {
        final parentIndex = _comments.indexWhere((c) => c.id == parentId);
        if (parentIndex != -1) {
          _comments[parentIndex].replies.add(newReply);
        }
        _replyController.clear();
        _replyingTo = null;
      });
    }

    if (mounted) {
      setState(() => _isSubmittingReply = false);
    }
  }

  Widget _buildCommentsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 40),
        Text(
          L10n.t('comments'),
          style: const TextStyle(
            color: Colors.white,
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 20),

        // Comment Input Box
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withOpacity(0.1)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CircleAvatar(
                    backgroundImage:
                        _currentUser != null &&
                            _currentUser!['photoURL']!.isNotEmpty
                        ? NetworkImage(_currentUser!['photoURL']!)
                        : null,
                    child:
                        _currentUser == null ||
                            _currentUser!['photoURL']!.isEmpty
                        ? const Icon(Icons.person)
                        : null,
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: TextField(
                      controller: _commentController,
                      style: const TextStyle(color: Colors.white),
                      maxLines: 3,
                      decoration: InputDecoration(
                        hintText: _currentUser == null
                            ? L10n.t('login_to_comment') ?? 'Đăng nhập để bình luận...'
                            : L10n.t('write_your_comment') ?? 'Viết bình luận của bạn...',
                        hintStyle: TextStyle(
                          color: Colors.white.withOpacity(0.4),
                        ),
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              ElevatedButton.icon(
                onPressed: _isSubmittingComment ? null : _handlePostComment,
                icon: _isSubmittingComment
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Icon(Icons.send, size: 18),
                label: Text(
                  _currentUser == null ? L10n.t('login_and_send') ?? 'Đăng nhập & Gửi' : L10n.t('send_comment') ?? 'Gửi bình luận',
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blueAccent,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 24),

        // Comments List
        if (_isLoadingComments)
          Center(child: CircularProgressIndicator())
        else if (_comments.isEmpty)
          Text(
            L10n.t('no_comments_yet') ?? 'Chưa có bình luận nào.',
            style: TextStyle(color: Colors.white54),
          )
        else
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _comments.length > _visibleComments
                ? _visibleComments
                : _comments.length,
            separatorBuilder: (context, index) =>
                const Divider(color: Colors.white12, height: 32),
            itemBuilder: (context, index) {
              final comment = _comments[index];
              return Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CircleAvatar(
                    backgroundImage: comment.userPhoto.isNotEmpty
                        ? NetworkImage(comment.userPhoto)
                        : null,
                    child: comment.userPhoto.isEmpty
                        ? const Icon(Icons.person)
                        : null,
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(
                              comment.userDisplayName,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              _formatTimeAgo(comment.timestamp),
                              style: TextStyle(
                                color: Colors.white.withOpacity(0.4),
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          comment.text,
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 15,
                            height: 1.5,
                          ),
                        ),

                        // Nút Trả lời
                        const SizedBox(height: 8),
                        GestureDetector(
                          onTap: () {
                            setState(() {
                              _replyingTo = _replyingTo == comment.id
                                  ? null
                                  : comment.id;
                              if (_replyingTo != null) {
                                _replyController.clear();
                              }
                            });
                          },
                          child: Text(
                            'Trả lời',
                            style: TextStyle(
                              color: Colors.blueAccent,
                              fontWeight: FontWeight.bold,
                              fontSize: 13,
                            ),
                          ),
                        ),

                        // Danh sách trả lời
                        if (comment.replies.isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.only(top: 12),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: comment.replies
                                  .map(
                                    (reply) => Padding(
                                      padding: const EdgeInsets.only(
                                        bottom: 12,
                                      ),
                                      child: Row(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          CircleAvatar(
                                            radius: 12,
                                            backgroundImage:
                                                reply.userPhoto.isNotEmpty
                                                ? NetworkImage(reply.userPhoto)
                                                : null,
                                            child: reply.userPhoto.isEmpty
                                                ? const Icon(
                                                    Icons.person,
                                                    size: 16,
                                                  )
                                                : null,
                                          ),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Column(
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              children: [
                                                Row(
                                                  children: [
                                                    Text(
                                                      reply.userDisplayName,
                                                      style: const TextStyle(
                                                        color: Colors.white,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                        fontSize: 14,
                                                      ),
                                                    ),
                                                    const SizedBox(width: 8),
                                                    Text(
                                                      _formatTimeAgo(
                                                        reply.timestamp,
                                                      ),
                                                      style: TextStyle(
                                                        color: Colors.white
                                                            .withOpacity(0.4),
                                                        fontSize: 11,
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                                const SizedBox(height: 4),
                                                Text(
                                                  reply.text,
                                                  style: const TextStyle(
                                                    color: Colors.white70,
                                                    fontSize: 14,
                                                    height: 1.4,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  )
                                  .toList(),
                            ),
                          ),

                        // Khung nhập trả lời
                        if (_replyingTo == comment.id)
                          Padding(
                            padding: const EdgeInsets.only(top: 12),
                            child: Row(
                              children: [
                                Expanded(
                                  child: TextField(
                                    controller: _replyController,
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 14,
                                    ),
                                    decoration: InputDecoration(
                                      hintText: _currentUser == null
                                          ? 'Đăng nhập để trả lời...'
                                          : 'Nhập câu trả lời...',
                                      hintStyle: TextStyle(
                                        color: Colors.white.withOpacity(0.4),
                                      ),
                                      filled: true,
                                      fillColor: Colors.white.withOpacity(0.05),
                                      contentPadding:
                                          const EdgeInsets.symmetric(
                                            horizontal: 16,
                                            vertical: 8,
                                          ),
                                      border: OutlineInputBorder(
                                        borderRadius: BorderRadius.circular(20),
                                        borderSide: BorderSide.none,
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 8),
                                IconButton(
                                  onPressed: _isSubmittingReply
                                      ? null
                                      : () => _handlePostReply(comment.id),
                                  icon: _isSubmittingReply
                                      ? const SizedBox(
                                          width: 16,
                                          height: 16,
                                          child: CircularProgressIndicator(
                                            strokeWidth: 2,
                                            color: Colors.blueAccent,
                                          ),
                                        )
                                      : const Icon(
                                          Icons.send,
                                          color: Colors.blueAccent,
                                          size: 20,
                                        ),
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                  ),
                ],
              );
            },
          ),

        if (!_isLoadingComments && _comments.length > _visibleComments)
          Padding(
            padding: const EdgeInsets.only(top: 16),
            child: TextButton(
              onPressed: () {
                setState(() {
                  _visibleComments += 5;
                });
              },
              child: Text(
                L10n.t('view_more_comments') ?? 'Xem thêm bình luận',
                style: TextStyle(color: Colors.blueAccent),
              ),
            ),
          ),
      ],
    );
  }

  String _formatTimeAgo(DateTime time) {
    final diff = DateTime.now().difference(time);
    if (diff.inDays > 365) return '${(diff.inDays / 365).floor()} năm trước';
    if (diff.inDays > 30) return '${(diff.inDays / 30).floor()} tháng trước';
    if (diff.inDays > 0) return '${diff.inDays} ngày trước';
    if (diff.inHours > 0) return '${diff.inHours} giờ trước';
    if (diff.inMinutes > 0) return '${diff.inMinutes} phút trước';
    return 'Vừa xong';
  }
}

class HoverPoster extends StatefulWidget {
  final Movie movie;
  const HoverPoster({super.key, required this.movie});

  @override
  State<HoverPoster> createState() => _HoverPosterState();
}

class _HoverPosterState extends State<HoverPoster> {
  bool _isHovered = false;
  bool _isLoadingImages = false;

  void _openGallery() async {
    if (_isLoadingImages) return;
    setState(() => _isLoadingImages = true);

    final images = await PhimApi.getMovieImages(widget.movie);
    
    if (mounted) {
      setState(() => _isLoadingImages = false);
      if (images.isNotEmpty) {
        Navigator.of(context).push(
          PageRouteBuilder(
            opaque: false,
            pageBuilder: (context, animation, secondaryAnimation) {
              return FadeTransition(
                opacity: animation,
                child: ImageGalleryViewer(images: images),
              );
            },
          ),
        );
      } else {
        UIUtils.showCustomSnackBar(context, 'Không tìm thấy hình ảnh nào từ TMDB', isError: true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: GestureDetector(
        onTap: _openGallery,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          width: 160,
          height: 240,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              if (_isHovered)
                BoxShadow(
                  color: Colors.white.withOpacity(0.3), // Glow effect
                  blurRadius: 20,
                  spreadRadius: 2,
                ),
            ],
          ),
          child: Stack(
            fit: StackFit.expand,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: CachedNetworkImage(
                  imageUrl: widget.movie.thumbUrl,
                  fit: BoxFit.cover,
                ),
              ),
              if (_isHovered || _isLoadingImages)
                Positioned.fill(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.4),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: _isLoadingImages 
                          ? const CircularProgressIndicator(color: Colors.amber)
                          : const Icon(Icons.zoom_in, color: Colors.white, size: 48),
                    ),
                  ),
                ),
              // Logo overlay watermark
              Positioned(
                bottom: 8,
                left: 8,
                child: AnimatedOpacity(
                  opacity: _isHovered ? 1.0 : 0.8,
                  duration: const Duration(milliseconds: 200),
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 6,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.6),
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(
                        color: Colors.white.withOpacity(0.2),
                        width: 0.5,
                      ),
                    ),
                    child: Image.asset('assets/logo.png', height: 28),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
  });

  @override
  State<HoverEpisodeButton> createState() => _HoverEpisodeButtonState();
}

class _HoverEpisodeButtonState extends State<HoverEpisodeButton> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              decoration: BoxDecoration(
                color: _isHovered
                    ? Colors.white.withOpacity(0.2)
                    : Colors.white.withOpacity(0.08),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _isHovered
                      ? Colors.white.withOpacity(0.5)
                      : Colors.white.withOpacity(0.15),
                  width: 1,
                ),
              ),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
                child: Text(
                  widget.text,
                  style: TextStyle(
                    color: _isHovered ? Colors.white : Colors.white70,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class HoverServerTab extends StatefulWidget {
  final String text;
  final bool isPremium;
  final bool isSelected;
  final VoidCallback onTap;

  const HoverServerTab({
    super.key,
    required this.text,
    required this.isPremium,
    required this.isSelected,
    required this.onTap,
  });

  @override
  State<HoverServerTab> createState() => _HoverServerTabState();
}

class _HoverServerTabState extends State<HoverServerTab> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    Color baseColor;
    Color borderColor;
    Color textColor;

    if (widget.isSelected) {
      baseColor = widget.isPremium
          ? Colors.amber.withOpacity(0.3)
          : Colors.blueAccent.withOpacity(0.3);
      borderColor = widget.isPremium ? Colors.amber : Colors.blueAccent;
      textColor = widget.isPremium ? Colors.amber : Colors.blue[300]!;
    } else {
      baseColor = _isHovered
          ? Colors.white.withOpacity(0.15)
          : Colors.white.withOpacity(0.05);
      borderColor = _isHovered
          ? Colors.white.withOpacity(0.4)
          : Colors.white.withOpacity(0.1);
      textColor = _isHovered ? Colors.white : Colors.white70;
    }

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              decoration: BoxDecoration(
                color: baseColor,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: borderColor, width: 1),
              ),
              child: Text(
                widget.text,
                style: TextStyle(
                  color: textColor,
                  fontWeight: widget.isSelected
                      ? FontWeight.bold
                      : FontWeight.normal,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
