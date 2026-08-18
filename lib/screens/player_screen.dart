import 'dart:async';
import 'dart:io';
import 'dart:ui';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:mytv4u_flutter/widgets/advanced_controls_panel.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:webview_windows/webview_windows.dart';

import 'package:window_manager/window_manager.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/services.dart';
import 'package:window_manager/window_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/movie.dart';
import '../api/motchill_scraper.dart';
import '../api/opensubtitles_api.dart';
import '../api/firebase_api.dart';
import '../api/config_api.dart';
import '../widgets/glass_container.dart';
import '../widgets/custom_title_bar.dart';

class PlayerScreen extends StatefulWidget {
  final List<Episode> episodes;
  final int currentEpisodeIndex;
  final String movieName;
  final String? imdbId;
  final int? season;
  final int? episode;
  final bool isLive;

  const PlayerScreen({
    super.key,
    required this.episodes,
    required this.currentEpisodeIndex,
    required this.movieName,
    this.imdbId,
    this.season,
    this.episode,
    this.isLive = false,
  });

  @override
  State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> with WindowListener {
  // media_kit
  late Player player;
  late VideoController controller;
  bool _hwAccel = true; // Bật mặc định
  double _subSize = 24.0;
  double _subOpacity = 0.3;
  bool _isPlayerInit = false;
  bool _isPlayerInitialized = false;
  bool _isDisposed = false;
  final List<StreamSubscription> _playerSubs = [];

  // webview_windows
  final _webController = WebviewController();
  bool _isWebviewInitialized = false;
  bool _isUsingWebview = false;
  bool _isExternalPlayerActive = false;

  // Player state
  String? errorMsg;
  late int _currentIndex;
  late String _currentUrl;
  bool _backgroundPlayback = false;
  bool _wasPlayingBeforeMinimize = false;
  bool _isPiPMode = false;
  Rect? _prePiPBounds;
  late String _currentTitle;

  // Fallback Domain State
  List<String> _fallbackDomains = ['sv.gboiz7.workers.dev'];
  int _currentFallbackDomainIndex = 0;

  // Motchill Servers
  List<Map<String, String>> _motchillServers = [];
  int _currentMotchillServerIndex = 0;
  bool _isLoadingServers = false;

  // UI state
  bool _showControls = true;
  bool _showEpisodePanel = false;
  
  Timer? _hideControlsTimer;

  // media_kit state
  Duration _position = Duration.zero;
  Duration _duration = Duration.zero;
  bool _isPlaying = false;
  double _volume = 100.0;
  bool _isFullscreen = false;
  bool _isVolumeHovered = false;
  bool _isSeekbarHovered = false;
  double? _hoverSeekFraction;
  final GlobalKey _seekbarKey = GlobalKey();

  List<AudioTrack> _audioTracks = [];
  List<SubtitleTrack> _subtitleTracks = [];
  List<SubtitleTrack> _openSubtitles = [];
  AudioTrack? _selectedAudioTrack;
  SubtitleTrack? _selectedSubtitleTrack;
  SubtitleTrack? _selectedSecondarySubtitleTrack;
  bool _autoNext = true;
  double _playbackSpeed = 1.0;
  final FocusNode _focusNode = FocusNode();
  Timer? _saveProgressTimer;

  @override
  void initState() {
    super.initState();
    windowManager.addListener(this);
    _focusNode.requestFocus();
    _startHideControlsTimer();
    _loadSettingsAndInit();

    _saveProgressTimer = Timer.periodic(const Duration(seconds: 10), (_) {
      if (_isPlaying && !_isUsingWebview) {
        _saveLocalProgress();
      }
    });
  }

  @override
  void onWindowEnterFullScreen() {
    if (mounted) setState(() => _isFullscreen = true);
  }

  @override
  void onWindowMinimize() async {
    if (!_backgroundPlayback && mounted && _isPlayerInitialized) {
      _wasPlayingBeforeMinimize = player.state.playing;
      if (_wasPlayingBeforeMinimize) {
        await player.pause();
      }
    }
  }

  @override
  void onWindowRestore() async {
    if (!_backgroundPlayback && mounted && _isPlayerInitialized && _wasPlayingBeforeMinimize) {
      await player.play();
    }
  }

  Future<void> _togglePiPMode() async {
    if (_isPiPMode) {
      setState(() => _isPiPMode = false);
      await windowManager.setAlwaysOnTop(false);
      if (_prePiPBounds != null) {
        await windowManager.setBounds(_prePiPBounds!);
      }
    } else {
      _prePiPBounds = await windowManager.getBounds();
      setState(() => _isPiPMode = true);
      await windowManager.setAlwaysOnTop(true);
      await windowManager.setSize(const Size(400, 225));
      await windowManager.setAlignment(Alignment.bottomRight);
    }
  }

  @override
  void onWindowLeaveFullScreen() {
    if (mounted) setState(() => _isFullscreen = false);
  }

  Future<void> _saveLocalProgress() async {
    if (_position.inMilliseconds > 0 && _duration.inMilliseconds > 0) {
      final prefs = await SharedPreferences.getInstance();
      final ep = widget.episodes[_currentIndex];
      final key = 'continue_${widget.movieName}_${ep.name}';
      await prefs.setInt(key, _position.inMilliseconds);
    }
  }

  Future<void> _loadSettingsAndInit() async {
    try {
      final domains = await ConfigApi.getFallbackDomains();
      if (mounted && domains.isNotEmpty) {
        setState(() {
          _fallbackDomains = domains;
        });
      }
    } catch (e) {
      debugPrint('Error loading fallback domains: $e');
    }

    final prefs = await SharedPreferences.getInstance();
    if (mounted) {
      setState(() {
        _hwAccel = prefs.getBool('enable_hw_accel') ?? true;
        _subSize = prefs.getDouble('sub_size') ?? 24.0;
        _subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;
      });
    }
    _initMediaKit();
    _initEpisode(widget.currentEpisodeIndex);
    if (mounted) {
      setState(() {
        _isPlayerInit = true;
      });
    }
  }

  bool _tryFallbackDomain() {
    if (_currentUrl.contains('dpdns.org') || _currentUrl.contains('workers.dev')) {
      final rawId = _currentUrl.split('/').last;
      _currentFallbackDomainIndex++;
      
      if (_currentFallbackDomainIndex < _fallbackDomains.length) {
         final newDomain = _fallbackDomains[_currentFallbackDomainIndex];
         final newUrl = 'https://$newDomain/$rawId';
         setState(() {
           _currentUrl = newUrl;
           errorMsg = null;
         });
         ScaffoldMessenger.of(context).showSnackBar(
             SnackBar(
               content: Text('Máy chủ quá tải. Đang chuyển sang luồng dự phòng ($newDomain)...'),
               backgroundColor: Colors.orange,
               duration: const Duration(seconds: 3),
             )
         );
         player.open(Media(newUrl));
         return true;
      }
    }
    return false;
  }

  void _initMediaKit() {
    player = Player(
      configuration: const PlayerConfiguration(
        bufferSize: 32 * 1024 * 1024,
        pitch: false,
      ),
    );
    
    // Tối ưu tốc độ tải luồng HLS/m3u8 (giảm độ trễ ban đầu)
    try {
      final platform = player.platform as dynamic;
      platform.setProperty('cache', 'yes');
      platform.setProperty('cache-pause', 'no'); // Phát ngay khi có dữ liệu, không chờ đầy buffer
      platform.setProperty('demuxer-max-bytes', '32M');
      platform.setProperty('demuxer-max-back-bytes', '10M');
      platform.setProperty('network-timeout', '10'); // Tránh treo lâu khi mạng lỗi
      platform.setProperty('demuxer-lavf-o-add', 'fflags=+fastseek');
    } catch (e) {
      debugPrint('Error setting MPV properties: $e');
    }

    controller = VideoController(
      player,
      configuration: VideoControllerConfiguration(
        enableHardwareAcceleration: _hwAccel,
      ),
    );

    _playerSubs.add(
      player.stream.error.listen((error) {
        if (mounted) {
          if (_tryFallbackDomain()) return;
          setState(() => errorMsg = error.toString());
        }
      }),
    );
    _playerSubs.add(
      player.stream.position.listen((pos) {
        if (mounted) setState(() => _position = pos);
      }),
    );
    _playerSubs.add(
      player.stream.duration.listen((dur) {
        if (mounted) setState(() => _duration = dur);
      }),
    );
    _playerSubs.add(
      player.stream.playing.listen((playing) {
        if (mounted) setState(() => _isPlaying = playing);
      }),
    );
    _playerSubs.add(
      player.stream.volume.listen((vol) {
        if (mounted) setState(() => _volume = vol);
      }),
    );
    _playerSubs.add(
      player.stream.completed.listen((completed) {
        if (completed && _autoNext) {
          final isNearEnd = _duration.inSeconds > 0 && 
              (_position.inSeconds >= _duration.inSeconds - 120);
          if (isNearEnd) {
            _playNextEpisode();
          } else {
            debugPrint('Luồng bị ngắt giữa chừng. Không tự động nhảy tập.');
            if (mounted) setState(() => errorMsg = 'Luồng bị ngắt kết nối. Vui lòng thử lại!');
          }
        }
      }),
    );
    _playerSubs.add(
      player.stream.tracks.listen((tracks) {
        if (mounted)
          setState(() {
            _audioTracks = tracks.audio;
            _subtitleTracks = tracks.subtitle;
          });
      }),
    );
    _playerSubs.add(
      player.stream.track.listen((track) {
        if (mounted)
          setState(() {
            _selectedAudioTrack = track.audio;
            _selectedSubtitleTrack = track.subtitle;
          });
      }),
    );
  }

  void _disposeMediaKit() {
    for (var sub in _playerSubs) {
      sub.cancel();
    }
    _playerSubs.clear();
    player.dispose();
  }

  void _toggleHwAccel(bool val) async {
    final pos = player.state.position;
    final isPlaying = player.state.playing;

    _disposeMediaKit();

    setState(() {
      _hwAccel = val;
    });

    _initMediaKit();
    await _playCurrentUrl(widget.episodes[_currentIndex]);
    await player.seek(pos);
    if (!isPlaying) player.pause();
  }

  void _updateSubtitlePosition() {
    try {
      final pos = _showControls ? '80' : '92';
      (player.platform as dynamic).setProperty('sub-pos', pos);
    } catch (e) {
      debugPrint('sub-pos update error: $e');
    }
  }

  void _startHideControlsTimer() {
    _hideControlsTimer?.cancel();
    _hideControlsTimer = Timer(const Duration(seconds: 4), () {
      if (mounted && !_showEpisodePanel) {
        if (_isPlaying || _isUsingWebview) {
          setState(() => _showControls = false);
          _updateSubtitlePosition();
        }
      }
    });
  }

  void _onHoverOrTap() {
    if (!_showControls) {
      setState(() => _showControls = true);
      _updateSubtitlePosition();
    }
    _startHideControlsTimer();
  }

  Future<void> _initEpisode(int index) async {
    if (index < 0 || index >= widget.episodes.length) return;
    setState(() {
      _currentIndex = index;
      errorMsg = null;
      _currentFallbackDomainIndex = 0; // Reset fallback domain
      _isLoadingServers = false;
      _openSubtitles = []; // clear old subs
      _selectedSubtitleTrack = null;
    });

    final ep = widget.episodes[index];
    String targetUrl = ep.m3u8Url.isNotEmpty ? ep.m3u8Url : ep.embedUrl;
    final epName = ep.name.toLowerCase().startsWith('tập')
        ? ep.name
        : 'Tập ${ep.name}';
    _currentTitle = '${widget.movieName} - $epName';

    // Fetch OpenSubtitles if this is a P2P stream (indicated by having imdbId)
    if (widget.imdbId != null && widget.imdbId!.isNotEmpty) {
      int? currentEpNum = widget.episode;
      // If no specific episode passed, try to parse it from the episode name if it's a TV show
      if (currentEpNum == null && epName.toLowerCase().contains('tập')) {
        final match = RegExp(r'tập\s*(\d+)').firstMatch(epName.toLowerCase());
        if (match != null) {
          currentEpNum = int.tryParse(match.group(1)!);
        }
      }

      OpenSubtitlesApi.fetchSubtitles(
        widget.imdbId!,
        season: widget.season,
        episode: currentEpNum,
      ).then((subs) {
        if (mounted && subs.isNotEmpty) {
          setState(() {
            _openSubtitles = subs;
          });
        }
      });
    }

    if (targetUrl.startsWith('motchill://')) {
      setState(() {
        _isLoadingServers = true;
      });

      final uri = Uri.parse(targetUrl);
      final svIndexStr = uri.queryParameters['sv'];
      final targetPath = targetUrl.split('?')[0];

      _motchillServers = await MotchillScraper.getEpisodeServers(targetPath);
      setState(() {
        _isLoadingServers = false;
        if (_motchillServers.isNotEmpty) {
          int svIndex = 0;
          if (svIndexStr != null) {
            svIndex = int.tryParse(svIndexStr) ?? 0;
            if (svIndex >= _motchillServers.length) svIndex = 0;
          }
          _currentMotchillServerIndex = svIndex;
          _currentUrl = _motchillServers[svIndex]['link']!;
        } else {
          _currentUrl = targetPath; // fallback
        }
      });
    } else {
      _motchillServers = [];
      _currentUrl = targetUrl;
    }

    // Proactively switch to the first working premium server config
    if (_fallbackDomains.isNotEmpty && (_currentUrl.contains('dpdns.org') || _currentUrl.contains('workers.dev'))) {
      final rawId = _currentUrl.split('/').last;
      _currentUrl = 'https://${_fallbackDomains.first}/$rawId';
    }

    await _playCurrentUrl(ep);
  }

  Future<void> _playCurrentUrl(Episode ep) async {
    bool isVideoFile =
        _currentUrl.contains('.m3u8') || _currentUrl.contains('.mp4');
    _isUsingWebview =
        !isVideoFile &&
        _currentUrl.startsWith('http') &&
        (_currentUrl.contains('embed') ||
            _currentUrl.contains('player') ||
            _currentUrl.contains('iframe') ||
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));

    if (_isUsingWebview) {
      player.pause();
      
      if (Platform.isWindows) {
        if (mounted) setState(() { _isExternalPlayerActive = true; });
        try {
          final bounds = await windowManager.getBounds();
          final title = "${widget.movieName} - ${ep.name}";
          final exeDir = File(Platform.resolvedExecutable).parent.path;
          var exePath = '$exeDir\\tv_web_player.exe';
          if (!File(exePath).existsSync()) {
            exePath = r"T:\Project\Phim\tv_web_player\bin\Release\net8.0-windows\tv_web_player.exe";
          }
          
          String? subtitlePath;
          if (widget.imdbId != null && widget.imdbId!.isNotEmpty) {
            try {
              int? inferredSeason = widget.season;
              int? currentEpNum = widget.episode;
              final epName = ep.name.toLowerCase().startsWith('tập') ? ep.name : 'Tập ${ep.name}';
              
              // 1. Try to extract exact Season and Episode from P2P slug (e.g. S2E3)
              final slugMatch = RegExp(r'^S(\d+)E(\d+)$', caseSensitive: false).firstMatch(ep.slug);
              if (slugMatch != null) {
                inferredSeason = int.tryParse(slugMatch.group(1)!);
                currentEpNum = int.tryParse(slugMatch.group(2)!);
              } else {
                // 2. Fallback: Parse episode from name (e.g. "Tập 3")
                if (currentEpNum == null && epName.toLowerCase().contains('tập')) {
                  final match = RegExp(r'tập\s*(\d+)').firstMatch(epName.toLowerCase());
                  if (match != null) {
                    currentEpNum = int.tryParse(match.group(1)!);
                  }
                }
                
                // 3. Fallback: Parse season from movie title (e.g. "Game of Thrones (Phần 2)")
                if (currentEpNum != null && inferredSeason == null) {
                  final seasonMatch = RegExp(r'(?:phần|mùa|season)\s*(\d+)', caseSensitive: false).firstMatch(widget.movieName);
                  if (seasonMatch != null) {
                    inferredSeason = int.tryParse(seasonMatch.group(1)!);
                  } else {
                    inferredSeason = 1;
                  }
                }
              }
              if (inferredSeason != null && currentEpNum != null) {
                subtitlePath = '${widget.imdbId!}:$inferredSeason:$currentEpNum';
              } else {
                subtitlePath = widget.imdbId!;
              }
            } catch (e) {
              debugPrint('Failed to process imdbId: $e');
            }
          }

          List<String> args = [
            _currentUrl,
            title,
            bounds.left.toInt().toString(),
            bounds.top.toInt().toString(),
            bounds.width.toInt().toString(),
            bounds.height.toInt().toString()
          ];
          if (subtitlePath != null) {
            args.add(subtitlePath);
          }
          
          final process = await Process.start(exePath, args);
          
          // Wait for the external player to close
          await process.exitCode;
          
          // No file to delete since we just passed the IMDB string
          if (mounted) setState(() { _isExternalPlayerActive = false; });
          
          // Go back to previous screen automatically when player is closed
          if (mounted) {
            Navigator.pop(context);
          }
          return;
        } catch (e) {
          debugPrint("Failed to start external player: $e");
          if (mounted) setState(() { _isExternalPlayerActive = false; });
        }
      }
      
      if (!_isWebviewInitialized) {
        await _webController.initialize();
        await _webController.setUserAgent(
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        );
        await _webController.setPopupWindowPolicy(
          WebviewPopupWindowPolicy.deny,
        );

        _webController.containsFullScreenElementChanged.listen((flag) async {
          if (mounted) {
            setState(() {
              _isFullscreen = flag;
            });
            await windowManager.setFullScreen(flag);
          }
        });

        _isWebviewInitialized = true;
      }
      await _webController.loadUrl(_currentUrl);
      if (mounted) setState(() {});
    } else {
      if (_isWebviewInitialized) {
        await _webController.loadUrl('about:blank'); // Clear webview
      }
      final Map<String, String> headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      };
      if (_currentUrl.contains('fptplay') || _currentUrl.contains('fplay')) {
        headers['Referer'] = 'https://fptplay.vn/';
      } else if (_currentUrl.contains('vtvgo') ||
          _currentUrl.contains('mediatech')) {
        headers['Referer'] = 'https://vtvgo.vn/';
      } else if (_currentUrl.contains('vtvprime')) {
        headers['Referer'] = 'https://vtvprime.vn/';
      } else if (_currentUrl.contains('thvli') ||
          _currentUrl.contains('vinhlong')) {
        headers['Referer'] = 'https://thvli.vn/';
      } else if (ep.m3u8Url.startsWith('motchill://')) {
        headers['Referer'] = 'https://motchillv.io/';
      }

      player.open(Media(_currentUrl, httpHeaders: headers), play: false);
      if (ep.slug == 'trailer' &&
          ep.embedUrl.isNotEmpty &&
          ep.embedUrl.startsWith('http')) {
        player.setAudioTrack(AudioTrack.uri(ep.embedUrl));
      }

      final prefs = await SharedPreferences.getInstance();
      final key = 'continue_${widget.movieName}_${ep.name}';
      final savedPos = prefs.getInt(key) ?? 0;

      if (savedPos > 5000 && mounted && ep.slug != 'trailer') {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (ctx) => Dialog(
            backgroundColor: Colors.transparent,
            elevation: 0,
            child: GlassContainer(
              width: 500,
              padding: const EdgeInsets.all(24),
              borderRadius: 16,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Tiếp tục xem?',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Bạn đã xem đến ${_formatDuration(Duration(milliseconds: savedPos))}. Bạn muốn xem tiếp hay xem lại từ đầu?',
                    style: const TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      TextButton(
                        onPressed: () {
                          Navigator.pop(ctx);
                          player.play();
                          prefs.remove(key);
                        },
                        child: const Text(
                          'Từ đầu',
                          style: TextStyle(color: Colors.white54, fontSize: 16),
                        ),
                      ),
                      const SizedBox(width: 16),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.blueAccent,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 24,
                            vertical: 12,
                          ),
                        ),
                        onPressed: () {
                          Navigator.pop(ctx);
                          if (player.state.duration.inMilliseconds > 0) {
                            player.seek(Duration(milliseconds: savedPos));
                            player.play();
                          } else {
                            // Wait for player to be ready before seeking
                            late StreamSubscription sub;
                            sub = player.stream.duration.listen((duration) {
                              if (duration.inMilliseconds > 0) {
                                player.seek(Duration(milliseconds: savedPos));
                                player.play();
                                sub.cancel();
                              }
                            });
                          }
                        },
                        child: const Text(
                          'Xem tiếp',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        );
      } else {
        player.play();
      }
    }
    _onHoverOrTap();
  }

  void _playNextEpisode() {
    if (_currentIndex + 1 < widget.episodes.length) {
      _initEpisode(_currentIndex + 1);
    }
  }

  void _toggleFullscreen() async {
    bool isFS = await windowManager.isFullScreen();
    await windowManager.setFullScreen(!isFS);
    if (mounted) {
      setState(() => _isFullscreen = !isFS);
    }
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    _saveProgressTimer?.cancel();
    _saveLocalProgress();
    _focusNode.dispose();
    _hideControlsTimer?.cancel();
    _disposeMediaKit();
    if (_isWebviewInitialized) _webController.dispose();
    super.dispose();
  }

  String _formatDuration(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, "0");
    String twoDigitMinutes = twoDigits(d.inMinutes.remainder(60));
    String twoDigitSeconds = twoDigits(d.inSeconds.remainder(60));
    if (d.inHours > 0) {
      return "${twoDigits(d.inHours)}:$twoDigitMinutes:$twoDigitSeconds";
    }
    return "$twoDigitMinutes:$twoDigitSeconds";
  }

  void _selectAudioTrack(AudioTrack track) {
    setState(() => _selectedAudioTrack = track);
    player.setAudioTrack(track);
    Navigator.pop(context);
  }

  void _selectSubtitleTrack(SubtitleTrack track) {
    setState(() => _selectedSubtitleTrack = track);
    player.setSubtitleTrack(track);
    Navigator.pop(context);
  }

  void _setPlaybackSpeed(double speed) {
    setState(() => _playbackSpeed = speed);
    player.setRate(speed);
    Navigator.pop(context);
  }

  String _getTrackShortName(dynamic track) {
    if (track.id == 'auto') return 'Tự động';
    if (track.id == 'no') return 'Tắt';
    return track.title ?? track.language ?? track.id ?? 'Không rõ';
  }

  String _getTrackFullName(dynamic track) {
    if (track.id == 'auto') return 'Tự động (Mặc định)';
    if (track.id == 'no') return 'Tắt';

    List<String> details = [];
    if (track.title != null && track.title.toString().trim().isNotEmpty)
      details.add(track.title);
    if (track.language != null && track.language.toString().trim().isNotEmpty)
      details.add('[${track.language}]');

    if (details.isEmpty) return 'Luồng ${track.id}';
    return details.join(' ');
  }

  Future<void> _addExternalSubtitle() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['srt', 'vtt', 'ass', 'ssa'],
    );
    if (result != null && result.files.single.path != null) {
      player.setSubtitleTrack(SubtitleTrack.uri(result.files.single.path!));
      if (Navigator.canPop(context)) Navigator.pop(context);
    }
  }

  Future<void> _addExternalAudio() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['m4a', 'mp3', 'aac', 'wav', 'flac'],
    );
    if (result != null && result.files.single.path != null) {
      player.setAudioTrack(AudioTrack.uri(result.files.single.path!));
      if (Navigator.canPop(context)) Navigator.pop(context);
    }
  }

  void _selectSecondarySubtitleTrack(SubtitleTrack track) {
    setState(() => _selectedSecondarySubtitleTrack = track);
    try {
      if (track.id == 'no' || track.id == 'auto') {
        (player.platform as dynamic).setProperty('secondary-sid', 'no');
        player.seek(player.state.position); // Force OSD refresh
      } else {
        (player.platform as dynamic).setProperty('secondary-sid', track.id);
        // Attempt to move primary subtitle up and secondary below it
        (player.platform as dynamic).setProperty('sub-pos', '85');
        (player.platform as dynamic).setProperty('secondary-sub-pos', '100');
      }
    } catch (e) {
      debugPrint('Secondary sub error: $e');
    }
    if (Navigator.canPop(context)) Navigator.pop(context);
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 2,
            child: Text(
              label,
              style: const TextStyle(color: Colors.white54, fontSize: 14),
            ),
          ),
          Expanded(
            flex: 3,
            child: SelectableText(
              value,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 14,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNextEpisodeOverlay() {
    bool hasNext = _currentIndex + 1 < widget.episodes.length;
    int remaining = _duration.inSeconds - _position.inSeconds;

    return Container(
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.8),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white24, width: 1),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                hasNext
                    ? 'Tập tiếp theo sẽ phát sau $remaining giây'
                    : 'Phim sẽ đóng sau $remaining giây',
                style: const TextStyle(color: Colors.white70, fontSize: 14),
              ),
              const SizedBox(height: 4),
              Text(
                hasNext ? widget.episodes[_currentIndex + 1].name : 'Kết thúc',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(width: 24),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blueAccent,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            onPressed: () {
              if (hasNext) {
                _playNextEpisode();
              } else {
                Navigator.pop(context);
              }
            },
            child: Text(hasNext ? 'Chuyển Tập Ngay' : 'Đóng'),
          ),
        ],
      ),
    );
  }

  void _showSettingsDialog() {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 600,
              height: 480,
              borderRadius: 24,
              color: const Color(0x1A000000),
              borderColor: const Color(0x33FFFFFF),
              blur: 40.0,
              child: DefaultTabController(
                length: 5,
                child: Column(
                  children: [
                    // Header with Tabs
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        border: Border(
                          bottom: BorderSide(
                            color: Colors.white.withOpacity(0.1),
                          ),
                        ),
                      ),
                      child: TabBar(
                        dividerColor: Colors.transparent,
                        indicatorColor: Colors.blueAccent,
                        labelColor: Colors.blueAccent,
                        unselectedLabelColor: Colors.white54,
                        isScrollable: true,
                        tabAlignment: TabAlignment.center,
                        tabs: [
                          const Tab(icon: Icon(Icons.speed), text: 'Chung'),
                          Tooltip(
                            message:
                                'Đang chọn: ${_selectedAudioTrack != null ? _getTrackShortName(_selectedAudioTrack) : "Tự động"}',
                            child: const Tab(
                              icon: Icon(Icons.audiotrack),
                              text: 'Âm thanh',
                            ),
                          ),
                          Tooltip(
                            message:
                                'Đang chọn: ${_selectedSubtitleTrack != null ? _getTrackShortName(_selectedSubtitleTrack) : "Tự động"}',
                            child: const Tab(
                              icon: Icon(Icons.subtitles),
                              text: 'Phụ đề chính',
                            ),
                          ),
                          Tooltip(
                            message:
                                'Đang chọn: ${_selectedSecondarySubtitleTrack != null ? _getTrackShortName(_selectedSecondarySubtitleTrack) : "Tắt"}',
                            child: const Tab(
                              icon: Icon(Icons.subtitles_outlined),
                              text: 'Phụ đề phụ',
                            ),
                          ),
                          const Tab(
                            icon: Icon(Icons.info_outline),
                            text: 'Thông tin',
                          ),
                        ],
                      ),
                    ),
                    // Content
                    Expanded(
                      child: TabBarView(
                        children: [
                          // Tab Chung
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [
                                ListTile(
                                  leading: const Icon(Icons.color_lens, color: Colors.blueAccent),
                                  title: const Text('Bộ lọc màu Video', style: TextStyle(color: Colors.white)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    setState(() => _activePanel = SidePanelMode.color);
                                  },
                                ),
                                const Divider(color: Colors.white24),
                                ListTile(
                                  title: const Text(
                                    'Tốc độ phát',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                  trailing: DropdownButton<double>(
                                    dropdownColor: Colors.grey[900],
                                    value: _playbackSpeed,
                                    style: const TextStyle(
                                      color: Colors.blueAccent,
                                    ),
                                    items: const [
                                      DropdownMenuItem(
                                        value: 0.5,
                                        child: Text('0.5x'),
                                      ),
                                      DropdownMenuItem(
                                        value: 1.0,
                                        child: Text('1x (Chuẩn)'),
                                      ),
                                      DropdownMenuItem(
                                        value: 1.25,
                                        child: Text('1.25x'),
                                      ),
                                      DropdownMenuItem(
                                        value: 1.5,
                                        child: Text('1.5x'),
                                      ),
                                      DropdownMenuItem(
                                        value: 2.0,
                                        child: Text('2x'),
                                      ),
                                    ],
                                    onChanged: (val) {
                                      if (val != null) {
                                        _setPlaybackSpeed(val);
                                        setTabState(() {});
                                      }
                                    },
                                  ),
                                ),
                                SwitchListTile(
                                  activeColor: Colors.blueAccent,
                                  title: const Text(
                                    'Tự động chuyển tập',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                  value: _autoNext,
                                  onChanged: (val) {
                                    setState(() => _autoNext = val);
                                    setTabState(() {});
                                  },
                                ),
                                SwitchListTile(
                                  activeColor: Colors.blueAccent,
                                  title: const Text(
                                    'Tăng tốc phần cứng (HW Accel)',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                  subtitle: const Text(
                                    'Tắt nếu gặp lỗi màn hình đen',
                                    style: TextStyle(
                                      color: Colors.white54,
                                      fontSize: 12,
                                    ),
                                  ),
                                  value: _hwAccel,
                                  onChanged: (val) {
                                    _toggleHwAccel(val);
                                    setTabState(() {});
                                  },
                                ),
                              ],
                            ),
                          ),
                          // Tab Âm thanh
                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
                              OutlinedButton.icon(
                                onPressed: _addExternalAudio,
                                icon: const Icon(Icons.add),
                                label: const Text('Thêm tệp âm thanh rời...'),
                                style: OutlinedButton.styleFrom(
                                  foregroundColor: Colors.blueAccent,
                                  side: const BorderSide(
                                    color: Colors.blueAccent,
                                  ),
                                ),
                              ),
                              const SizedBox(height: 16),
                              ..._audioTracks.map((track) {
                                final isSelected =
                                    track.id == _selectedAudioTrack?.id;
                                return HoverableTrackItem(
                                  title: _getTrackFullName(track),
                                  isSelected: isSelected,
                                  onTap: () => _selectAudioTrack(track),
                                );
                              }),
                            ],
                          ),
                          // Tab Phụ đề chính
                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
                              OutlinedButton.icon(
                                onPressed: _addExternalSubtitle,
                                icon: const Icon(Icons.add),
                                label: const Text('Thêm tệp phụ đề rời...'),
                                style: OutlinedButton.styleFrom(
                                  foregroundColor: Colors.blueAccent,
                                  side: const BorderSide(
                                    color: Colors.blueAccent,
                                  ),
                                ),
                              ),
                              const SizedBox(height: 16),
                              ...[..._subtitleTracks, ..._openSubtitles].map((
                                track,
                              ) {
                                final isSelected =
                                    track.id == _selectedSubtitleTrack?.id;
                                return HoverableTrackItem(
                                  title: _getTrackFullName(track),
                                  isSelected: isSelected,
                                  onTap: () => _selectSubtitleTrack(track),
                                );
                              }),
                            ],
                          ),
                          // Tab Phụ đề phụ
                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
                              OutlinedButton.icon(
                                onPressed: _addExternalSubtitle,
                                icon: const Icon(Icons.add),
                                label: const Text('Thêm tệp phụ đề rời...'),
                                style: OutlinedButton.styleFrom(
                                  foregroundColor: Colors.blueAccent,
                                  side: const BorderSide(
                                    color: Colors.blueAccent,
                                  ),
                                ),
                              ),
                              const SizedBox(height: 16),
                              ...[..._subtitleTracks, ..._openSubtitles].map((
                                track,
                              ) {
                                final isSelected =
                                    track.id ==
                                    _selectedSecondarySubtitleTrack?.id;
                                return HoverableTrackItem(
                                  title: _getTrackFullName(track),
                                  isSelected: isSelected,
                                  onTap: () =>
                                      _selectSecondarySubtitleTrack(track),
                                );
                              }),
                            ],
                          ),
                          // Tab Thông tin
                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 24,
                            ),
                            children: [
                              _buildInfoRow('Tên phim', widget.movieName),
                              _buildInfoRow(
                                'Tập đang phát',
                                widget.episodes[_currentIndex].name,
                              ),
                              _buildInfoRow(
                                'Thời lượng',
                                _formatDuration(_duration),
                              ),
                              if (!_isUsingWebview)
                                _buildInfoRow(
                                  'Độ phân giải',
                                  '${player.state.width ?? "Đang tải"} x ${player.state.height ?? "Đang tải"}',
                                ),
                              _buildInfoRow(
                                'Nguồn phát',
                                _isUsingWebview
                                    ? 'Trình duyệt Web (Embed)'
                                    : 'Trình phát Video gốc',
                              ),
                              if (_isUsingWebview)
                                _buildInfoRow('URL', _currentUrl),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildGlassIconButton(
    IconData icon,
    VoidCallback onTap, {
    double size = 24,
    String? tooltip,
  }) {
    return Tooltip(
      message: tooltip ?? '',
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(50),
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.all(8),
            child: Icon(icon, color: Colors.white, size: size),
          ),
        ),
      ),
    );
  }

  Widget _buildMotchillServerList() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
      child: Row(
        children: [
          const Text(
            'Nguồn phụ: ',
            style: TextStyle(
              color: Colors.white70,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _motchillServers.asMap().entries.map((e) {
                  final isSelected = e.key == _currentMotchillServerIndex;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: ActionChip(
                      label: Text(
                        e.value['name']!,
                        style: TextStyle(
                          color: isSelected ? Colors.white : Colors.white70,
                        ),
                      ),
                      backgroundColor: isSelected
                          ? Colors.blueAccent
                          : Colors.white.withOpacity(0.1),
                      side: BorderSide.none,
                      onPressed: () {
                        setState(() {
                          _currentMotchillServerIndex = e.key;
                          _currentUrl = e.value['link']!;
                          _playCurrentUrl(widget.episodes[_currentIndex]);
                        });
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isExternalPlayerActive) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CircularProgressIndicator(color: Colors.blueAccent),
              const SizedBox(height: 20),
              const Text(
                "Đang mở trình phát độ phân giải cao...\n(Bấm ESC bên cửa sổ kia để thoát)",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white, fontSize: 16),
              ),
            ],
          ),
        ),
      );
    }

    if (!_isPlayerInit) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: CircularProgressIndicator(color: Colors.white)),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Focus(
        focusNode: _focusNode,
        autofocus: true,
        onKeyEvent: (node, event) {
          if (event is KeyDownEvent) {
            if (event.logicalKey == LogicalKeyboardKey.escape) {
              if (_isFullscreen) _toggleFullscreen();
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.space) {
              player.playOrPause();
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.arrowRight) {
              player.seek(_position + const Duration(seconds: 10));
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.arrowLeft) {
              player.seek(_position - const Duration(seconds: 10));
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.arrowUp) {
              player.setVolume((_volume + 10).clamp(0, 100));
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.arrowDown) {
              player.setVolume((_volume - 10).clamp(0, 100));
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.keyF) {
              _toggleFullscreen();
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.keyM) {
              player.setVolume(_volume > 0 ? 0 : 100);
              return KeyEventResult.handled;
            }
            if (event.logicalKey == LogicalKeyboardKey.keyN) {
              if (_currentIndex + 1 < widget.episodes.length) {
                _playNextEpisode();
              }
              return KeyEventResult.handled;
            }
          }
          return KeyEventResult.ignored;
        },
        child: MouseRegion(
          onHover: (_) => _onHoverOrTap(),
          child: GestureDetector(
            onTap: _onHoverOrTap,
            child: Stack(
              fit: StackFit.expand,
              children: [
                // 1. Video Layer
                if (_isLoadingServers)
                  const Center(
                    child: CircularProgressIndicator(color: Colors.blueAccent),
                  )
                else if (_isUsingWebview && _isWebviewInitialized)
                  Webview(_webController)
                else
                  Center(
                    child: Video(
                      controller: controller,
                      controls: NoVideoControls, // Tắt controls mặc định
                      subtitleViewConfiguration: SubtitleViewConfiguration(
                        style: TextStyle(
                          fontSize: _subSize,
                          color: Colors.white,
                          backgroundColor: Colors.black.withOpacity(_subOpacity),
                        ),
                      ),
                    ),
                  ),

                // Error Overlay
                if (errorMsg != null)
                  Center(
                    child: GlassContainer(
                      width: 450,
                      borderRadius: 16,
                      color: Colors.black.withOpacity(0.7),
                      borderColor: Colors.redAccent.withOpacity(0.3),
                      blur: 20,
                      child: Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(
                              Icons.warning_amber_rounded,
                              color: Colors.redAccent,
                              size: 48,
                            ),
                            const SizedBox(height: 16),
                            const Text(
                              'Thông Báo Trình Phát',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              errorMsg!.toLowerCase().contains('truehd')
                                  ? 'Phim chứa định dạng âm thanh Dolby TrueHD nhưng bản dựng mpv hiện tại chưa được tích hợp codec này.\n\n👉 Cách xử lý: Bấm vào nút Cài đặt (⚙️) -> Tab Âm thanh, và đổi sang một luồng âm thanh khác (như AC3 hoặc AAC) để có tiếng.'
                                  : errorMsg!.contains('11470')
                                  ? 'Không thể tải dữ liệu Torrent.\n\nNguyên nhân: Link torrent này hiện không có đủ người chia sẻ (Seeders) hoặc bị lỗi kết nối mạng ngang hàng. Vui lòng thử chọn một server/chất lượng khác.'
                                  : 'Đã xảy ra lỗi:\n$errorMsg',
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                color: Colors.white70,
                                fontSize: 14,
                              ),
                            ),
                            const SizedBox(height: 24),
                            ElevatedButton.icon(
                              onPressed: () => setState(() => errorMsg = null),
                              icon: const Icon(Icons.close),
                              label: const Text('Đóng thông báo'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.redAccent.withOpacity(
                                  0.2,
                                ),
                                foregroundColor: Colors.white,
                                elevation: 0,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                // Next Episode Overlay (Near End)
                if (!widget.isLive &&
                    _duration.inSeconds > 0 &&
                    (_duration.inSeconds - _position.inSeconds) <= 30 &&
                    !_isUsingWebview)
                  Positioned(
                    bottom: 100,
                    right: 32,
                    child: TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0.0, end: 1.0),
                      duration: const Duration(milliseconds: 300),
                      builder: (context, val, child) {
                        return Opacity(
                          opacity: val,
                          child: Transform.translate(
                            offset: Offset(0, 20 * (1 - val)),
                            child: child,
                          ),
                        );
                      },
                      child: _buildNextEpisodeOverlay(),
                    ),
                  ),

                // 2. Controls Layer
                AnimatedOpacity(
                  opacity: _showControls || _showEpisodePanel ? 1.0 : 0.0,
                  duration: const Duration(milliseconds: 300),
                  child: IgnorePointer(
                    ignoring: !_showControls && !_showEpisodePanel,
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        // Top Bar (YouTube Gradient)
                        Positioned(
                          top: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            padding: EdgeInsets.only(
                              top: _isFullscreen ? 16 : 40,
                              bottom: 20,
                              left: 16,
                              right: 16,
                            ),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomCenter,
                                colors: [
                                  Colors.black.withOpacity(0.85),
                                  Colors.black.withOpacity(0.3),
                                  Colors.transparent,
                                ],
                              ),
                            ),
                            child: Row(
                              children: [
                                IconButton(
                                  icon: const Icon(
                                    Icons.arrow_back,
                                    color: Colors.white,
                                    size: 24,
                                  ),
                                  onPressed: () async {
                                    if (_isFullscreen) {
                                      await windowManager.setFullScreen(false);
                                    }
                                    if (mounted) Navigator.pop(context);
                                  },
                                  tooltip: 'Quay lại',
                                ),
                                const SizedBox(width: 12),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 16,
                                    vertical: 8,
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.black.withOpacity(0.65),
                                    borderRadius: BorderRadius.circular(20),
                                    border: Border.all(
                                      color: Colors.white24,
                                      width: 1,
                                    ),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black.withOpacity(0.4),
                                        blurRadius: 8,
                                      ),
                                    ],
                                  ),
                                  child: Text(
                                    _currentTitle,
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 14,
                                      fontWeight: FontWeight.bold,
                                    ),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),

                        // Motchill Server List Bar
                        if (_motchillServers.isNotEmpty && !_isLoadingServers)
                          Positioned(
                            top: _isFullscreen ? 70 : 94,
                            left: 16,
                            right: 16,
                            child: GlassContainer(
                              borderRadius: 16,
                              color: Colors.black.withOpacity(0.4),
                              blur: 20,
                              child: _buildMotchillServerList(),
                            ),
                          ),

                        // Bottom Controls (Latest YouTube Style)
                        if (!_isUsingWebview)
                          Positioned(
                            bottom: 0,
                            left: 0,
                            right: 0,
                            child: Container(
                              padding: const EdgeInsets.only(
                                top: 24,
                                bottom: 16,
                                left: 16,
                                right: 16,
                              ),
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.bottomCenter,
                                  end: Alignment.topCenter,
                                  colors: [
                                    Colors.black.withOpacity(0.9),
                                    Colors.black.withOpacity(0.4),
                                    Colors.transparent,
                                  ],
                                ),
                              ),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  if (!_isPiPMode)
                                  // YouTube Red Seekbar with Hover Time Tooltip
                                  MouseRegion(
                                    key: _seekbarKey,
                                    onEnter: (_) => setState(
                                      () => _isSeekbarHovered = true,
                                    ),
                                    onHover: (event) {
                                      final RenderBox? box =
                                          _seekbarKey.currentContext
                                                  ?.findRenderObject()
                                              as RenderBox?;
                                      if (box != null &&
                                          _duration.inMilliseconds > 0) {
                                        final localPos = box.globalToLocal(
                                          event.position,
                                        );
                                        final fraction =
                                            (localPos.dx / box.size.width)
                                                .clamp(0.0, 1.0);
                                        setState(
                                          () => _hoverSeekFraction = fraction,
                                        );
                                      }
                                    },
                                    onExit: (_) => setState(() {
                                      _isSeekbarHovered = false;
                                      _hoverSeekFraction = null;
                                    }),
                                    child: Stack(
                                      clipBehavior: Clip.none,
                                      children: [
                                        Row(
                                          children: [
                                            Expanded(
                                              child: SliderTheme(
                                                data: SliderTheme.of(context).copyWith(
                                                  trackHeight: 3,
                                                  thumbShape:
                                                      const RoundSliderThumbShape(
                                                        enabledThumbRadius: 6,
                                                      ),
                                                  overlayShape:
                                                      const RoundSliderOverlayShape(
                                                        overlayRadius: 14,
                                                      ),
                                                  activeTrackColor: const Color(
                                                    0xFFFF0000,
                                                  ),
                                                  inactiveTrackColor:
                                                      Colors.white24,
                                                  thumbColor: const Color(
                                                    0xFFFF0000,
                                                  ),
                                                  overlayColor: const Color(
                                                    0xFFFF0000,
                                                  ).withOpacity(0.2),
                                                ),
                                                child: Slider(
                                                  value: _position
                                                      .inMilliseconds
                                                      .toDouble()
                                                      .clamp(
                                                        0,
                                                        _duration.inMilliseconds
                                                            .toDouble(),
                                                      ),
                                                  max:
                                                      _duration.inMilliseconds
                                                              .toDouble() >
                                                          0
                                                      ? _duration.inMilliseconds
                                                            .toDouble()
                                                      : 1.0,
                                                  onChanged: (val) =>
                                                      player.seek(
                                                        Duration(
                                                          milliseconds: val
                                                              .toInt(),
                                                        ),
                                                      ),
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        if (_isSeekbarHovered &&
                                            _hoverSeekFraction != null &&
                                            _duration.inMilliseconds > 0)
                                          Positioned(
                                            left:
                                                (_hoverSeekFraction! *
                                                        (MediaQuery.of(
                                                              context,
                                                            ).size.width -
                                                            64))
                                                    .clamp(
                                                      0.0,
                                                      MediaQuery.of(
                                                            context,
                                                          ).size.width -
                                                          100,
                                                    ),
                                            top: -36,
                                            child: Container(
                                              padding:
                                                  const EdgeInsets.symmetric(
                                                    horizontal: 10,
                                                    vertical: 5,
                                                  ),
                                              decoration: BoxDecoration(
                                                color: Colors.black.withOpacity(
                                                  0.9,
                                                ),
                                                borderRadius:
                                                    BorderRadius.circular(8),
                                                border: Border.all(
                                                  color: Colors.white24,
                                                  width: 1,
                                                ),
                                                boxShadow: [
                                                  BoxShadow(
                                                    color: Colors.black
                                                        .withOpacity(0.5),
                                                    blurRadius: 6,
                                                  ),
                                                ],
                                              ),
                                              child: Text(
                                                _formatDuration(
                                                  Duration(
                                                    milliseconds:
                                                        (_hoverSeekFraction! *
                                                                _duration
                                                                    .inMilliseconds)
                                                            .toInt(),
                                                  ),
                                                ),
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontSize: 12,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                            ),
                                          ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  if (_isPiPMode)
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        IconButton(
                                          icon: Icon(
                                            _isPlaying ? Icons.pause : Icons.play_arrow,
                                            color: Colors.white,
                                            size: 40,
                                          ),
                                          onPressed: () => player.playOrPause(),
                                        ),
                                        const SizedBox(width: 20),
                                        IconButton(
                                          icon: const Icon(
                                            Icons.fullscreen,
                                            color: Colors.white,
                                            size: 40,
                                          ),
                                          onPressed: _togglePiPMode,
                                        ),
                                      ],
                                    ),
                                  if (!_isPiPMode)
                                  // YouTube Button Row
                                  Row(
                                    children: [
                                      // Play / Pause Circle Pill
                                      Container(
                                        width: 38,
                                        height: 38,
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.2),
                                          shape: BoxShape.circle,
                                        ),
                                        child: IconButton(
                                          icon: Icon(
                                            _isPlaying
                                                ? Icons.pause
                                                : Icons.play_arrow,
                                            color: Colors.white,
                                            size: 22,
                                          ),
                                          onPressed: () => player.playOrPause(),
                                          padding: EdgeInsets.zero,
                                          tooltip: _isPlaying
                                              ? 'Tạm dừng (Space)'
                                              : 'Phát (Space)',
                                        ),
                                      ),
                                      const SizedBox(width: 10),
                                      // Rewind -10s Circle Pill
                                      Container(
                                        width: 38,
                                        height: 38,
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.2),
                                          shape: BoxShape.circle,
                                        ),
                                        child: IconButton(
                                          icon: const Icon(
                                            Icons.replay_10,
                                            color: Colors.white,
                                            size: 20,
                                          ),
                                          onPressed: () => player.seek(
                                            _position -
                                                const Duration(seconds: 10),
                                          ),
                                          padding: EdgeInsets.zero,
                                          tooltip: 'Lùi 10s (←)',
                                        ),
                                      ),
                                      const SizedBox(width: 10),
                                      // Forward +10s Circle Pill
                                      Container(
                                        width: 38,
                                        height: 38,
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.2),
                                          shape: BoxShape.circle,
                                        ),
                                        child: IconButton(
                                          icon: const Icon(
                                            Icons.forward_10,
                                            color: Colors.white,
                                            size: 20,
                                          ),
                                          onPressed: () => player.seek(
                                            _position +
                                                const Duration(seconds: 10),
                                          ),
                                          padding: EdgeInsets.zero,
                                          tooltip: 'Tới 10s (→)',
                                        ),
                                      ),
                                      const SizedBox(width: 10),
                                      // Expandable Volume Button on Hover
                                      MouseRegion(
                                        onEnter: (_) => setState(
                                          () => _isVolumeHovered = true,
                                        ),
                                        onExit: (_) => setState(
                                          () => _isVolumeHovered = false,
                                        ),
                                        child: AnimatedContainer(
                                          duration: const Duration(
                                            milliseconds: 200,
                                          ),
                                          width: _isVolumeHovered ? 160 : 38,
                                          height: 38,
                                          decoration: BoxDecoration(
                                            color: Colors.white.withOpacity(
                                              0.2,
                                            ),
                                            borderRadius: BorderRadius.circular(
                                              20,
                                            ),
                                          ),
                                          child: Row(
                                            children: [
                                              IconButton(
                                                icon: Icon(
                                                  _volume == 0
                                                      ? Icons.volume_off
                                                      : Icons.volume_up,
                                                  color: Colors.white,
                                                  size: 20,
                                                ),
                                                onPressed: () =>
                                                    player.setVolume(
                                                      _volume == 0 ? 100 : 0,
                                                    ),
                                                padding: EdgeInsets.zero,
                                                constraints:
                                                    const BoxConstraints(
                                                      minWidth: 38,
                                                      minHeight: 38,
                                                    ),
                                                tooltip: 'Âm lượng',
                                              ),
                                              if (_isVolumeHovered)
                                                Expanded(
                                                  child: Padding(
                                                    padding:
                                                        const EdgeInsets.only(
                                                          right: 12,
                                                        ),
                                                    child: SliderTheme(
                                                      data:
                                                          SliderTheme.of(
                                                            context,
                                                          ).copyWith(
                                                            trackHeight: 3,
                                                            thumbShape:
                                                                const RoundSliderThumbShape(
                                                                  enabledThumbRadius:
                                                                      5,
                                                                ),
                                                            overlayShape:
                                                                SliderComponentShape
                                                                    .noOverlay,
                                                            activeTrackColor:
                                                                Colors.white,
                                                            inactiveTrackColor:
                                                                Colors.white30,
                                                            thumbColor:
                                                                Colors.white,
                                                          ),
                                                      child: Slider(
                                                        value: _volume,
                                                        max: 100,
                                                        onChanged: (val) =>
                                                            player.setVolume(
                                                              val,
                                                            ),
                                                      ),
                                                    ),
                                                  ),
                                                ),
                                            ],
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 10),
                                      // Time Display Pill (4:04 / 14:40)
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 16,
                                          vertical: 8,
                                        ),
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.2),
                                          borderRadius: BorderRadius.circular(
                                            20,
                                          ),
                                        ),
                                        child: Text(
                                          '${_formatDuration(_position)} / ${_formatDuration(_duration)}',
                                          style: const TextStyle(
                                            color: Colors.white,
                                            fontSize: 13,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                      const Spacer(),
                                      // Right Controls Capsule Container
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 12,
                                          vertical: 6,
                                        ),
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.2),
                                          borderRadius: BorderRadius.circular(
                                            20,
                                          ),
                                        ),
                                        child: Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            // Next Episode Button (Right side)
                                            IconButton(
                                              icon: const Icon(
                                                Icons.skip_next,
                                                color: Colors.white,
                                                size: 22,
                                              ),
                                              onPressed: _playNextEpisode,
                                              tooltip: 'Tập tiếp theo',
                                              padding: const EdgeInsets.all(4),
                                              constraints:
                                                  const BoxConstraints(),
                                            ),
                                            const SizedBox(width: 10),
                                            // Episode List Button
                                            IconButton(
                                              icon: const Icon(
                                                Icons.format_list_bulleted,
                                                color: Colors.white,
                                                size: 20,
                                              ),
                                              onPressed: () => setState(
                                                () => _showEpisodePanel =
                                                    !_showEpisodePanel,
                                              ),
                                              tooltip: 'Danh sách tập',
                                              padding: const EdgeInsets.all(4),
                                              constraints:
                                                  const BoxConstraints(),
                                            ),
                                            const SizedBox(width: 10),

                                            // Settings Gear Button
                                            IconButton(
                                              icon: const Icon(
                                                Icons.settings,
                                                color: Colors.white,
                                                size: 20,
                                              ),
                                              onPressed: _showSettingsDialog,
                                              tooltip: 'Cài đặt',
                                              padding: const EdgeInsets.all(4),
                                              constraints:
                                                  const BoxConstraints(),
                                            ),
                                            const SizedBox(width: 10),
                                            // Fullscreen Button
                                            IconButton(
                                              icon: Icon(
                                                _isFullscreen
                                                    ? Icons.fullscreen_exit
                                                    : Icons.fullscreen,
                                                color: Colors.white,
                                                size: 22,
                                              ),
                                              onPressed: _toggleFullscreen,
                                              tooltip: 'Toàn màn hình',
                                              padding: const EdgeInsets.all(4),
                                              constraints:
                                                  const BoxConstraints(),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),



                // 3. Episode Selection Panel (Right Sidebar)
                if (!_isPiPMode)
                AnimatedPositioned(
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeInOut,
                  top: 0,
                  bottom: 0,
                  right: _showEpisodePanel ? 0 : -350,
                  width: 350,
                  child: GlassContainer(
                    borderRadius: 0,
                    color: Colors.black.withOpacity(0.7),
                    blur: 40,
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              'Chọn tập',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            IconButton(
                              icon: const Icon(
                                Icons.close,
                                color: Colors.white,
                              ),
                              onPressed: () =>
                                  setState(() => _showEpisodePanel = false),
                            ),
                          ],
                        ),
                        const Divider(color: Colors.white24, height: 32),
                        Expanded(
                          child: GridView.builder(
                            gridDelegate:
                                const SliverGridDelegateWithFixedCrossAxisCount(
                                  crossAxisCount: 4,
                                  crossAxisSpacing: 8,
                                  mainAxisSpacing: 8,
                                  childAspectRatio: 1.5,
                                ),
                            itemCount: widget.episodes.length,
                            itemBuilder: (context, index) {
                              final isCurrent = index == _currentIndex;
                              return Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(8),
                                  onTap: () {
                                    _initEpisode(index);
                                    setState(() => _showEpisodePanel = false);
                                  },
                                  child: Container(
                                    decoration: BoxDecoration(
                                      color: isCurrent
                                          ? Colors.blueAccent.withOpacity(0.4)
                                          : Colors.white10,
                                      borderRadius: BorderRadius.circular(8),
                                      border: Border.all(
                                        color: isCurrent
                                            ? Colors.blueAccent
                                            : Colors.transparent,
                                      ),
                                    ),
                                    alignment: Alignment.center,
                                    child: Text(
                                      widget.episodes[index].name,
                                      style: TextStyle(
                                        color: isCurrent
                                            ? Colors.blueAccent
                                            : Colors.white,
                                        fontWeight: isCurrent
                                            ? FontWeight.bold
                                            : FontWeight.normal,
                                      ),
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                // Window Title Bar (Positioned at VERY TOP of Stack so Close/Minimize/Maximize ALWAYS work!)
                if (!_isFullscreen && !_isPiPMode)
                  const Positioned(
                    top: 0,
                    left: 0,
                    right: 0,
                    height: 36,
                    child: CustomTitleBar(),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class HoverableTrackItem extends StatefulWidget {
  final String title;
  final bool isSelected;
  final VoidCallback onTap;

  const HoverableTrackItem({
    Key? key,
    required this.title,
    required this.isSelected,
    required this.onTap,
  }) : super(key: key);

  @override
  State<HoverableTrackItem> createState() => _HoverableTrackItemState();
}

class _HoverableTrackItemState extends State<HoverableTrackItem> {
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovering = true),
      onExit: (_) => setState(() => _isHovering = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          margin: const EdgeInsets.only(bottom: 6),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: widget.isSelected
                ? Colors.blueAccent.withOpacity(0.15)
                : _isHovering
                ? Colors.white.withOpacity(0.05)
                : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: widget.isSelected
                  ? Colors.blueAccent.withOpacity(0.5)
                  : _isHovering
                  ? Colors.white.withOpacity(0.3)
                  : Colors.transparent,
              width: 1.5,
            ),
          ),
          child: Row(
            children: [
              AnimatedContainer(
                duration: const Duration(milliseconds: 150),
                width: _isHovering && !widget.isSelected ? 8 : 0,
              ),
              Expanded(
                child: Text(
                  widget.title,
                  style: TextStyle(
                    color: widget.isSelected
                        ? Colors.blueAccent
                        : (_isHovering ? Colors.white : Colors.white70),
                    fontWeight: widget.isSelected || _isHovering
                        ? FontWeight.bold
                        : FontWeight.normal,
                  ),
                ),
              ),
              if (widget.isSelected)
                const Icon(
                  Icons.check_circle,
                  color: Colors.blueAccent,
                  size: 20,
                ),
            ],
          ),
        ),
      ),
    );
  }
}
