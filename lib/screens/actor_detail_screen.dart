import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../api/phim_api.dart';
import '../models/movie.dart';
import '../widgets/hover_movie_card.dart';
import '../widgets/custom_title_bar.dart';
import '../widgets/glass_container.dart';
import 'movie_detail_screen.dart';

class ActorDetailScreen extends StatefulWidget {
  final String actorId;
  final String actorName;

  const ActorDetailScreen({
    super.key,
    required this.actorId,
    required this.actorName,
  });

  @override
  State<ActorDetailScreen> createState() => _ActorDetailScreenState();
}

class _ActorDetailScreenState extends State<ActorDetailScreen> {
  bool _isLoadingInfo = true;
  Map<String, dynamic>? _actorInfo;
  
  List<Movie> _availableMovies = [];
  bool _isSearching = true;
  int _totalMovies = 0;
  int _checkedMovies = 0;
  bool _isBioExpanded = false;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  @override
  void dispose() {
    _isSearching = false; // Dừng tiến trình ngầm khi thoát màn hình
    super.dispose();
  }

  Future<void> _fetchData() async {
    // Lấy thông tin diễn viên
    final info = await PhimApi.getActorDetails(widget.actorId);
    if (mounted) {
      setState(() {
        _actorInfo = info;
        _isLoadingInfo = false;
      });
    }

    // Lấy danh sách phim từ TMDB và bắt đầu dò ngầm
    final credits = await PhimApi.getActorMovieCredits(widget.actorId);
    if (mounted) {
      setState(() {
        _totalMovies = credits.length;
        if (_totalMovies == 0) _isSearching = false;
      });
      if (_totalMovies > 0) {
        _startProgressiveSearch(credits);
      }
    }
  }

  Future<void> _startProgressiveSearch(List<Map<String, dynamic>> tmdbMovies) async {
    int maxConcurrent = 3; // Kiểm tra 3 phim cùng lúc
    int currentIndex = 0;
    
    Future<void> searchWorker() async {
      while (currentIndex < tmdbMovies.length && _isSearching && mounted) {
        int indexToProcess = currentIndex;
        currentIndex++;
        
        final tmdbMovie = tmdbMovies[indexToProcess];
        final title = tmdbMovie['original_title'] ?? tmdbMovie['title'] ?? '';
        final year = tmdbMovie['release_date']?.toString().split('-')[0] ?? '';
        
        if (title.isNotEmpty) {
          try {
            final results = await PhimApi.searchMovies(title);
            Movie? match;
            for (var m in results) {
              if (m.originalName.toLowerCase() == title.toLowerCase() || 
                  m.name.toLowerCase() == (tmdbMovie['title'] ?? '').toString().toLowerCase()) {
                // Ưu tiên năm trùng khớp hoặc API của mình không có năm
                if (year.isEmpty || m.year == year || m.year.isEmpty) {
                  match = m;
                  break;
                }
              }
            }
            if (match != null && mounted && _isSearching) {
              setState(() {
                if (!_availableMovies.any((e) => e.slug == match!.slug)) {
                   _availableMovies.add(match!);
                }
              });
            }
          } catch (_) {}
        }
        
        if (mounted && _isSearching) {
          setState(() {
            _checkedMovies++;
          });
        }
      }
    }

    List<Future> workers = [];
    for (int i = 0; i < maxConcurrent; i++) {
      workers.add(searchWorker());
    }
    await Future.wait(workers);
    
    if (mounted && _isSearching) {
      setState(() {
        _isSearching = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final String profilePath = _actorInfo?['profile_path'] != null 
        ? 'https://image.tmdb.org/t/p/w500${_actorInfo!['profile_path']}' 
        : '';
        
    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      body: Stack(
        children: [
          // Background
          if (profilePath.isNotEmpty)
            Positioned.fill(
              child: CachedNetworkImage(
                imageUrl: profilePath,
                fit: BoxFit.cover,
                color: Colors.black.withOpacity(0.7),
                colorBlendMode: BlendMode.darken,
              ),
            ),
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 50.0, sigmaY: 50.0),
              child: Container(color: Colors.black.withOpacity(0.5)),
            ),
          ),
          
          // Content
          Column(
            children: [
              const CustomTitleBar(),
              Expanded(
                child: _isLoadingInfo 
                    ? const Center(child: CircularProgressIndicator())
                    : CustomScrollView(
                        slivers: [
                          _buildActorInfo(profilePath),
                          _buildMoviesGrid(),
                        ],
                      ),
              ),
            ],
          ),
          
          // Back Button
          Positioned(
            top: 48,
            left: 24,
            child: Container(
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.3),
                shape: BoxShape.circle,
              ),
              child: IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.white, size: 24),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActorInfo(String profilePath) {
    final bio = _actorInfo?['biography']?.toString().trim() ?? '';
    final isLongBio = bio.length > 300;
    final displayBio = (_isBioExpanded || !isLongBio) 
        ? bio 
        : '${bio.substring(0, 300)}...';

    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(40, 40, 40, 40),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Ảnh đại diện
            if (profilePath.isNotEmpty)
              ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: CachedNetworkImage(
                  imageUrl: profilePath,
                  width: 250,
                  height: 375,
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Container(color: Colors.white10),
                  errorWidget: (context, url, error) => Container(color: Colors.white10, child: const Icon(Icons.person, size: 80, color: Colors.white24)),
                ),
              )
            else
              Container(
                width: 250, height: 375,
                decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(16)),
                child: const Icon(Icons.person, size: 80, color: Colors.white24),
              ),
            
            const SizedBox(width: 40),
            
            // Thông tin
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    widget.actorName,
                    style: const TextStyle(
                      fontSize: 48,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      height: 1.1,
                      shadows: [Shadow(color: Colors.black, blurRadius: 10)],
                    ),
                  ),
                  const SizedBox(height: 16),
                  Wrap(
                    spacing: 12,
                    runSpacing: 12,
                    children: [
                      if (_actorInfo?['birthday'] != null)
                        _buildBadge(Icons.cake, 'Ngày sinh: ${_actorInfo!['birthday']}'),
                      if (_actorInfo?['place_of_birth'] != null)
                        _buildBadge(Icons.location_on, '${_actorInfo!['place_of_birth']}'),
                      if (_actorInfo?['known_for_department'] != null)
                        _buildBadge(Icons.work, '${_actorInfo!['known_for_department']}'),
                    ],
                  ),
                  const SizedBox(height: 24),
                  if (bio.isNotEmpty) ...[
                    const Text('Tiểu sử', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 12),
                    Text(
                      displayBio,
                      style: TextStyle(fontSize: 15, color: Colors.white.withOpacity(0.8), height: 1.6),
                    ),
                    if (isLongBio)
                      TextButton(
                        onPressed: () => setState(() => _isBioExpanded = !_isBioExpanded),
                        child: Text(_isBioExpanded ? 'Thu gọn' : 'Xem thêm', style: const TextStyle(color: Colors.amber)),
                      ),
                  ]
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildBadge(IconData icon, String text) {
    return GlassContainer(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      borderRadius: 20,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: Colors.amber),
          const SizedBox(width: 8),
          Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }

  Widget _buildMoviesGrid() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 40),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('Phim trên hệ thống', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                const SizedBox(width: 16),
                if (_isSearching)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.amber.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.amber.withOpacity(0.5)),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const SizedBox(
                          width: 12, height: 12,
                          child: CircularProgressIndicator(color: Colors.amber, strokeWidth: 2),
                        ),
                        const SizedBox(width: 8),
                        Text('Đang dò tìm... ($_checkedMovies/$_totalMovies)', style: const TextStyle(color: Colors.amber, fontSize: 13, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  )
                else
                  Text('(${_availableMovies.length} phim)', style: const TextStyle(color: Colors.white54, fontSize: 16)),
              ],
            ),
            const SizedBox(height: 24),
            if (_availableMovies.isEmpty && !_isSearching)
              const Padding(
                padding: EdgeInsets.only(top: 40),
                child: Center(child: Text('Chưa có phim nào của diễn viên này trên hệ thống.', style: TextStyle(color: Colors.white54, fontSize: 16))),
              )
            else
              GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 5,
                  childAspectRatio: 0.65,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                ),
                itemCount: _availableMovies.length,
                itemBuilder: (context, index) {
                  final movie = _availableMovies[index];
                  return HoverMovieCard(
                    movie: movie,
                    heroTag: 'actor_movie_${movie.slug}',
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => MovieDetailScreen(slug: movie.slug, heroTag: 'actor_movie_${movie.slug}', initialMovie: movie)),
                      );
                    },
                  );
                },
              ),
            const SizedBox(height: 60),
          ],
        ),
      ),
    );
  }
}
