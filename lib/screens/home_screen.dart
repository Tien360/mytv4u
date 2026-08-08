import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';
import 'dart:async';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/movie.dart';
import '../api/phim_api.dart';
import '../api/auth_api.dart';
import '../api/firebase_api.dart';
import '../api/cinemeta_api.dart';
import '../widgets/glass_search_bar.dart';
import '../widgets/hover_movie_card.dart';
import 'movie_detail_screen.dart';
import '../api/update_api.dart';
import '../widgets/update_dialog.dart';

class HomeScreen extends StatefulWidget {
  final Function(String, String)? onNavigateToExplore; // Callback để chuyển tab Khám Phá

  const HomeScreen({super.key, this.onNavigateToExplore});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ScrollController _scrollController = ScrollController();
  final ScrollController _historyScrollController = ScrollController();
  Timer? _heroTimer;
  List<Movie> _heroMovies = [];
  int _currentHeroIndex = 0;
  bool _isLoadingHero = true;
  bool _isLoggedIn = false;
  List<Map<String, dynamic>> _history = [];

  // Định nghĩa các hàng
  final List<Map<String, dynamic>> _sections = [
    {'title': 'Phim Quốc Tế Thịnh Hành (Stremio)', 'type': 'stremio', 'slug': 'top'},
    {'title': 'Phim Lẻ Mới Cập Nhật', 'type': 'category', 'slug': 'phim-le'},
    {'title': 'Phim Bộ Mới Cập Nhật', 'type': 'category', 'slug': 'phim-bo'},
    {'title': 'Phim Hàn Quốc', 'type': 'country', 'slug': 'han-quoc'},
    {'title': 'Phim Trung Quốc', 'type': 'country', 'slug': 'trung-quoc'},
    {'title': 'Phim Âu Mỹ', 'type': 'country', 'slug': 'au-my'},
    {'title': 'Phim Hoạt Hình', 'type': 'category', 'slug': 'hoat-hinh'},
    {'title': 'TV Shows', 'type': 'category', 'slug': 'tv-shows'},
  ];

  @override
  void initState() {
    super.initState();
    _loadHeroMovies();
    _loadHistory();
    
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkSilentUpdate();
    });
  }

  Future<void> _checkSilentUpdate() async {
    final updateInfo = await UpdateApi.checkForUpdate();
    if (updateInfo != null && mounted) {
      showDialog(
        context: context,
        barrierDismissible: !updateInfo.isForceUpdate,
        builder: (context) => UpdateDialog(updateInfo: updateInfo),
      );
    }
  }

  Future<void> _loadHeroMovies() async {
    try {
      final movies = await PhimApi.getNewUpdatedMovies(page: 1);
      if (mounted) {
        // Filter movies that have ALL required rich metadata (like the web app)
        final validMovies = movies.where((m) => m.description.isNotEmpty && m.thumbUrl.isNotEmpty && m.posterUrl.isNotEmpty).toList();
        
        List<Movie> selected = validMovies.isNotEmpty ? validMovies.take(5).toList() : movies.take(5).toList();
        
        setState(() {
          _heroMovies = selected;
          _isLoadingHero = false;
        });
        _startHeroTimer();

        // Fetch backdrops for movies that lack a true horizontal poster
        for (int i = 0; i < selected.length; i++) {
          final m = selected[i];
          if (m.posterUrl == m.thumbUrl) {
            final isTvSeries = m.episodes.isNotEmpty && m.episodes.first.items.length > 1;
            final backdrop = await PhimApi.getMovieTmdbBackdrop(m.name, m.originalName, m.year, isTvSeries);
            if (mounted && backdrop != null && backdrop.isNotEmpty) {
              setState(() {
                _heroMovies[i] = m.copyWith(posterUrl: backdrop);
              });
            }
          }
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoadingHero = false);
      }
    }
  }

  void _startHeroTimer() {
    _heroTimer?.cancel();
    _heroTimer = Timer.periodic(const Duration(seconds: 8), (timer) {
      if (_heroMovies.isNotEmpty && mounted) {
        setState(() {
          _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
        });
      }
    });
  }

  @override
  void dispose() {
    _heroTimer?.cancel();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _loadHistory() async {
    final user = await AuthApi.getCurrentUser();
    if (user != null) {
      _isLoggedIn = true;
    }
    // Always load history, even anonymously
    final history = await FirebaseApi.getContinueWatching();
    if (mounted) {
      setState(() {
        _history = history;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent, // Nền trong suốt để thấy glassmorphism của main_screen
      body: SafeArea(
        child: RefreshIndicator(
        onRefresh: () async {
          setState(() {
            _isLoadingHero = true;
            _heroMovies.clear();
          });
          await _loadHeroMovies();
          await _loadHistory();
        },
        child: ListView.builder(
          controller: _scrollController,
          itemCount: _sections.length + 2, // Hero + History + Sections
          itemBuilder: (context, index) {
            if (index == 0) return _buildHeroCarousel();
            if (index == 1) return _buildHistorySection();
            
            final section = _sections[index - 2];
            return HorizontalMovieSection(
              title: section['title'],
              fetchType: section['type'],
              slug: section['slug'],
              onSeeMore: () {
                if (widget.onNavigateToExplore != null) {
                  widget.onNavigateToExplore!(section['type'], section['slug']);
                }
              },
            );
          },
        ),
      ),
      ),
    );
  }

  Widget _buildHeroCarousel() {
    if (_isLoadingHero) {
      return const SizedBox(
        height: 400,
        child: Center(child: CircularProgressIndicator()),
      );
    }
    if (_heroMovies.isEmpty) return const SizedBox.shrink();

    return Listener(
      onPointerSignal: (pointerSignal) {
        if (pointerSignal is PointerScrollEvent) {
          if (pointerSignal.scrollDelta.dy > 0 || pointerSignal.scrollDelta.dx > 0) {
            setState(() {
              _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
            });
            _startHeroTimer();
          } else if (pointerSignal.scrollDelta.dy < 0 || pointerSignal.scrollDelta.dx < 0) {
            setState(() {
              _currentHeroIndex = (_currentHeroIndex - 1 + _heroMovies.length) % _heroMovies.length;
            });
            _startHeroTimer();
          }
        }
      },
      child: Stack(
        children: [
          // Hero Background and Info with Fade Transition
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 800),
            transitionBuilder: (Widget child, Animation<double> animation) {
              return FadeTransition(opacity: animation, child: child);
            },
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1400),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(15, 32, 15, 48),
                  child: Container(
                    height: MediaQuery.of(context).size.height * 0.65 < 450 ? 450 : MediaQuery.of(context).size.height * 0.65,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(24),
                    ),
                    clipBehavior: Clip.antiAlias,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  // Image
                  Hero(
                    tag: 'banner_${_heroMovies[_currentHeroIndex].slug}',
                    child: CachedNetworkImage(
                      imageUrl: _heroMovies[_currentHeroIndex].posterUrl.isNotEmpty ? _heroMovies[_currentHeroIndex].posterUrl : _heroMovies[_currentHeroIndex].thumbUrl,
                      fit: BoxFit.cover,
                      alignment: Alignment.topCenter,
                      errorWidget: (context, url, error) => Container(color: Colors.grey[900], child: const Icon(Icons.broken_image)),
                    ),
                  ),
                  
                  // Gradient for hero-overlay (Left to Right)
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.centerLeft,
                        end: Alignment.centerRight,
                        colors: [
                          const Color(0xFF0F111A).withOpacity(1.0),
                          const Color(0xFF0F111A).withOpacity(0.6),
                          const Color(0xFF0F111A).withOpacity(0.0),
                        ],
                        stops: const [0.0, 0.45, 1.0],
                      ),
                    ),
                  ),
                  
                  // Content
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Padding(
                      padding: const EdgeInsets.only(left: 64, right: 64), // padding: 0 4rem
                      child: SizedBox(
                        width: MediaQuery.of(context).size.width * 0.5,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Title
                            Text(
                              _heroMovies[_currentHeroIndex].name,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 40, // 2.5rem
                                fontWeight: FontWeight.bold,
                                height: 1.1,
                              ),
                            ),
                            const SizedBox(height: 8),
                            // Original Name
                            Text(
                              _heroMovies[_currentHeroIndex].originalName,
                              style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 16),
                            ),
                            const SizedBox(height: 16),
                            // Tags
                            Row(
                              children: [
                                if (_heroMovies[_currentHeroIndex].quality.isNotEmpty) ...[
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Theme.of(context).primaryColor,
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(_heroMovies[_currentHeroIndex].quality, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
                                  ),
                                  const SizedBox(width: 8),
                                ],
                                if (_heroMovies[_currentHeroIndex].currentEpisode.isNotEmpty) ...[
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.white.withOpacity(0.15),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(_heroMovies[_currentHeroIndex].currentEpisode, style: const TextStyle(color: Colors.white, fontSize: 12)),
                                  ),
                                  const SizedBox(width: 8),
                                ],
                                if (_heroMovies[_currentHeroIndex].year.isNotEmpty) ...[
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.white.withOpacity(0.15),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(_heroMovies[_currentHeroIndex].year.toString(), style: const TextStyle(color: Colors.white, fontSize: 12)),
                                  ),
                                  const SizedBox(width: 8),
                                ],
                                ..._heroMovies[_currentHeroIndex].genres.take(3).map((genre) => Padding(
                                  padding: const EdgeInsets.only(right: 8.0),
                                  child: Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.white.withOpacity(0.15),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(genre, style: const TextStyle(color: Colors.white, fontSize: 12)),
                                  ),
                                )),
                              ],
                            ),
                            if (_heroMovies[_currentHeroIndex].description.isNotEmpty) ...[
                              const SizedBox(height: 16),
                              // Description
                              Text(
                                _heroMovies[_currentHeroIndex].description.replaceAll(RegExp(r'<[^>]*>|&[^;]+;'), '').trim(),
                                style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 14, height: 1.6),
                                maxLines: 4,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                            const SizedBox(height: 24),
                            // Circular Play Button
                            GestureDetector(
                              onTap: () => _navigateToDetail(_heroMovies[_currentHeroIndex], 'banner_${_heroMovies[_currentHeroIndex].slug}'),
                              child: Container(
                                width: 70,
                                height: 70,
                                decoration: BoxDecoration(
                                  color: Theme.of(context).primaryColor,
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(
                                      color: Theme.of(context).primaryColor.withOpacity(0.4),
                                      blurRadius: 15,
                                      offset: const Offset(0, 4),
                                    ),
                                  ],
                                ),
                                child: const Icon(Icons.play_arrow, size: 36, color: Colors.white), 
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  
                  // Thumbnails
                  Positioned(
                    bottom: 32,
                    right: 32,
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: List.generate(_heroMovies.length > 5 ? 5 : _heroMovies.length, (index) {
                        final movie = _heroMovies[index];
                        final isSelected = _currentHeroIndex == index;
                        return GestureDetector(
                          onTap: () {
                            setState(() {
                              _currentHeroIndex = index;
                            });
                            _startHeroTimer(); // Reset timer when clicked
                          },
                          child: AnimatedOpacity(
                            duration: const Duration(milliseconds: 300),
                            opacity: isSelected ? 1.0 : 0.6,
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 300),
                              width: 120,
                              height: 68,
                              margin: const EdgeInsets.only(left: 12),
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(8),
                                border: isSelected ? Border.all(color: Theme.of(context).primaryColor, width: 2) : Border.all(color: Colors.transparent, width: 2),
                                boxShadow: isSelected ? [
                                  BoxShadow(
                                    color: Theme.of(context).primaryColor.withOpacity(0.3),
                                    blurRadius: 15,
                                    offset: const Offset(0, 4),
                                  )
                                ] : [],
                                image: DecorationImage(
                                  image: CachedNetworkImageProvider(movie.posterUrl.isNotEmpty ? movie.posterUrl : movie.thumbUrl),
                                  fit: BoxFit.cover,
                                  alignment: Alignment.topCenter,
                                ),
                              ),
                            ),
                          ),
                        );
                      }),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
          ),
        ],
      ),
    );
  }

  Widget _buildHistorySection() {
    if (_history.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              'Tiếp Tục Xem',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
            ),
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 160,
            child: Stack(
              children: [
                ListView.builder(
                  controller: _historyScrollController,
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  itemCount: _history.length,
                  itemBuilder: (context, index) {
                    final item = _history[index];
                    return GestureDetector(
                      onTap: () {
                        final movie = Movie(
                          name: item['name'],
                          originalName: '',
                          slug: item['slug'],
                          thumbUrl: item['thumbUrl'],
                          posterUrl: '',
                          currentEpisode: item['currentEpisode'],
                          quality: '',
                          language: '',
                          year: '',
                          time: '',
                          description: '',
                          genres: [],
                          countries: [],
                          directors: [],
                          casts: [],
                          episodes: [],
                          source: item['source'] ?? 'nguonc'
                        );
                        _navigateToDetail(movie, 'history_${item['slug']}');
                      },
                      child: Container(
                        width: 240,
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        child: Stack(
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Hero(
                                tag: 'history_${item['slug']}',
                                child: CachedNetworkImage(
                                  imageUrl: item['thumbUrl'],
                                  fit: BoxFit.cover,
                                  width: 240,
                                  height: 160,
                                  errorWidget: (context, url, error) => Container(color: Colors.grey[800], child: const Icon(Icons.broken_image)),
                                ),
                              ),
                            ),
                            Container(
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(8),
                                gradient: LinearGradient(
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                  colors: [Colors.transparent, Colors.black.withOpacity(0.9)],
                                ),
                              ),
                            ),
                            Positioned(
                              bottom: 12,
                              left: 12,
                              right: 12,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    item['name'],
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'Đang xem: ${item['currentEpisode']}',
                                    style: const TextStyle(color: Colors.blueAccent, fontSize: 12, fontWeight: FontWeight.w500),
                                  ),
                                ],
                              ),
                            ),
                            const Center(
                              child: Icon(Icons.play_circle_outline, color: Colors.white54, size: 48),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
                Positioned(
                  left: 0,
                  top: 0,
                  bottom: 0,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.5),
                        shape: BoxShape.circle,
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_left, size: 30, color: Colors.white),
                        onPressed: () {
                          _historyScrollController.animateTo(
                            _historyScrollController.offset - 500,
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        },
                      ),
                    ),
                  ),
                ),
                Positioned(
                  right: 0,
                  top: 0,
                  bottom: 0,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.5),
                        shape: BoxShape.circle,
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_right, size: 30, color: Colors.white),
                        onPressed: () {
                          _historyScrollController.animateTo(
                            _historyScrollController.offset + 500,
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        },
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _navigateToDetail(Movie movie, [String? heroTag]) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => MovieDetailScreen(slug: movie.slug, heroTag: heroTag, initialMovie: movie)),
    ).then((_) {
      _loadHistory();
    });
  }
}

class HorizontalMovieSection extends StatefulWidget {
  final String title;
  final String fetchType; 
  final String slug;
  final VoidCallback onSeeMore;

  const HorizontalMovieSection({
    super.key,
    required this.title,
    required this.fetchType,
    required this.slug,
    required this.onSeeMore,
  });

  @override
  State<HorizontalMovieSection> createState() => _HorizontalMovieSectionState();
}

class _HorizontalMovieSectionState extends State<HorizontalMovieSection> {
  List<Movie> _movies = [];
  bool _isLoading = true;
  final ScrollController _sectionScrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    try {
      List<Movie> result;
      if (widget.fetchType == 'stremio') {
        result = await CinemetaApi.getTopMovies();
      } else if (widget.fetchType == 'country') {
        result = await PhimApi.getMoviesByCountry(widget.slug, page: 1);
      } else {
        result = await PhimApi.getMoviesByCategory(widget.slug, page: 1);
      }
      if (mounted) {
        setState(() {
          _movies = result.take(15).toList();
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_isLoading && _movies.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  widget.title,
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                TextButton(
                  onPressed: widget.onSeeMore,
                  child: const Text('Xem thêm >', style: TextStyle(color: Colors.blueAccent)),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),
          SizedBox(
            height: 360,
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : Stack(
                    children: [
                      ListView.builder(
                        controller: _sectionScrollController,
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(horizontal: 24),
                        itemCount: _movies.length,
                        itemBuilder: (context, index) {
                          final movie = _movies[index];
                          return Container(
                            width: 240,
                            margin: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
                            child: HoverMovieCard(
                              movie: movie,
                              heroTag: 'category_${widget.title}_${movie.slug}',
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(builder: (_) => MovieDetailScreen(slug: movie.slug, heroTag: 'category_${widget.title}_${movie.slug}', initialMovie: movie)),
                                );
                              },
                            ),
                          );
                        },
                      ),
                      Positioned(
                        left: 0,
                        top: 0,
                        bottom: 0,
                        child: Center(
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.5),
                              shape: BoxShape.circle,
                            ),
                            child: IconButton(
                              icon: const Icon(Icons.chevron_left, size: 30, color: Colors.white),
                              onPressed: () {
                                _sectionScrollController.animateTo(
                                  _sectionScrollController.offset - 500,
                                  duration: const Duration(milliseconds: 300),
                                  curve: Curves.easeInOut,
                                );
                              },
                            ),
                          ),
                        ),
                      ),
                      Positioned(
                        right: 0,
                        top: 0,
                        bottom: 0,
                        child: Center(
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.5),
                              shape: BoxShape.circle,
                            ),
                            child: IconButton(
                              icon: const Icon(Icons.chevron_right, size: 30, color: Colors.white),
                              onPressed: () {
                                _sectionScrollController.animateTo(
                                  _sectionScrollController.offset + 500,
                                  duration: const Duration(milliseconds: 300),
                                  curve: Curves.easeInOut,
                                );
                              },
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
          ),
        ],
      ),
    );
  }
}
