import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../api/phim_api.dart';
import '../models/movie.dart';
import 'movie_detail_screen.dart';
import '../widgets/glass_search_bar.dart';
import '../widgets/glass_container.dart';
import '../widgets/hover_movie_card.dart';
import '../utils/l10n.dart';

class ExploreScreen extends StatefulWidget {
  const ExploreScreen({super.key});

  @override
  State<ExploreScreen> createState() => ExploreScreenState();
}

class ExploreScreenState extends State<ExploreScreen> {
  List<Movie> _movies = [];
  bool _isLoading = false;
  int _page = 1;

  String _currentFilterType = 'category'; // category, genre, country
  String _currentSlug = 'phim-le';

  final ScrollController _scrollController = ScrollController();

  List<Map<String, String>> get _categories => [
    {'name': L10n.t('category_movies'), 'slug': 'phim-le'},
    {'name': L10n.t('category_series'), 'slug': 'phim-bo'},
    {'name': L10n.t('category_anime'), 'slug': 'hoat-hinh'},
    {'name': L10n.t('category_tv_shows'), 'slug': 'tv-shows'},
  ];

  List<Map<String, String>> get _genres => [
    {'name': L10n.t('genre_all'), 'slug': ''},
    {'name': L10n.t('genre_action'), 'slug': 'hanh-dong'},
    {'name': L10n.t('genre_romance'), 'slug': 'tinh-cam'},
    {'name': L10n.t('genre_comedy'), 'slug': 'hai-huoc'},
    {'name': L10n.t('genre_historical'), 'slug': 'co-trang'},
    {'name': L10n.t('genre_psychological'), 'slug': 'tam-ly'},
    {'name': L10n.t('genre_criminal'), 'slug': 'hinh-su'},
    {'name': L10n.t('genre_scifi'), 'slug': 'vien-tuong'},
    {'name': L10n.t('genre_horror'), 'slug': 'kinh-di'},
    {'name': L10n.t('genre_animation'), 'slug': 'hoat-hinh'}
  ];

  List<Map<String, String>> get _countries => [
    {'name': L10n.t('country_all'), 'slug': ''},
    {'name': L10n.t('category_korean'), 'slug': 'han-quoc'},
    {'name': L10n.t('category_chinese'), 'slug': 'trung-quoc'},
    {'name': L10n.t('category_western'), 'slug': 'au-my'},
    {'name': L10n.t('country_vietnam'), 'slug': 'viet-nam'},
    {'name': L10n.t('country_japan'), 'slug': 'nhat-ban'},
    {'name': L10n.t('country_thailand'), 'slug': 'thai-lan'}
  ];

  void setFilter(String type, String slug) {
    if (slug.isEmpty) return; // Ignore "All" selections if they just clear it
    if (_currentFilterType == type && _currentSlug == slug) return;
    setState(() {
      _currentFilterType = type;
      _currentSlug = slug;
    });
    _fetchData(reset: true);
  }

  @override
  void initState() {
    super.initState();
    _fetchData();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200) {
        _loadMore();
      }
    });
  }

  Future<void> _fetchData({bool reset = false}) async {
    if (_isLoading) return;
    if (reset) {
      _page = 1;
      setState(() {
        _movies.clear();
      });
    }
    setState(() => _isLoading = true);

    try {
      List<Movie> newMovies = [];
      if (_currentFilterType == 'category') {
        newMovies = await PhimApi.getMoviesByCategory(_currentSlug, page: _page);
      } else if (_currentFilterType == 'genre') {
        newMovies = await PhimApi.getMoviesByGenre(_currentSlug, page: _page);
      } else if (_currentFilterType == 'country') {
        newMovies = await PhimApi.getMoviesByCountry(_currentSlug, page: _page);
      }

      if (mounted) {
        setState(() {
          _movies.addAll(newMovies);
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _loadMore() {
    if (!_isLoading) {
      _page++;
      _fetchData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        top: false, // We handle top padding manually in SearchBar
        child: Column(
          children: [
            _buildFiltersBar(),
            Expanded(
              child: GridView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(16),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 5,
                  childAspectRatio: 0.65,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                ),
                itemCount: _movies.length + (_isLoading ? 1 : 0),
                itemBuilder: (context, index) {
                  if (index == _movies.length) {
                    return Center(child: CircularProgressIndicator());
                  }
                  final movie = _movies[index];
                  return HoverMovieCard(
                    movie: movie,
                    heroTag: 'explore_${movie.slug}',
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => MovieDetailScreen(slug: movie.slug, heroTag: 'explore_${movie.slug}', initialMovie: movie)),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFiltersBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            ..._categories.map((cat) {
              final isSelected = _currentFilterType == 'category' && _currentSlug == cat['slug'];
              return Padding(
                padding: const EdgeInsets.only(right: 8.0),
                child: ChoiceChip(
                  label: Text(
                    cat['name']!,
                    style: TextStyle(
                      color: isSelected ? Colors.white : Colors.white70,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                  selected: isSelected,
                  selectedColor: const Color(0xFF3B82F6),
                  backgroundColor: const Color(0x33FFFFFF),
                  side: BorderSide.none,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  onSelected: (selected) {
                    if (selected) setFilter('category', cat['slug']!);
                  },
                ),
              );
            }),
            const SizedBox(width: 4),
            GlassContainer(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              borderRadius: 20,
              blur: 20,
              height: 40,
              color: const Color(0x1A000000),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _currentFilterType == 'genre' ? _currentSlug : '',
                  dropdownColor: const Color(0xFF1E1E24),
                  icon: const Icon(Icons.arrow_drop_down, color: Colors.white70),
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                  items: _genres.map((opt) {
                    return DropdownMenuItem<String>(
                      value: opt['slug'],
                      child: Text(opt['name']!),
                    );
                  }).toList(),
                  onChanged: (val) {
                    if (val != null && val.isNotEmpty) setFilter('genre', val);
                  },
                ),
              ),
            ),
            const SizedBox(width: 8),
            GlassContainer(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              borderRadius: 20,
              blur: 20,
              height: 40,
              color: const Color(0x1A000000),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _currentFilterType == 'country' ? _currentSlug : '',
                  dropdownColor: const Color(0xFF1E1E24),
                  icon: const Icon(Icons.arrow_drop_down, color: Colors.white70),
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                  items: _countries.map((opt) {
                    return DropdownMenuItem<String>(
                      value: opt['slug'],
                      child: Text(opt['name']!),
                    );
                  }).toList(),
                  onChanged: (val) {
                    if (val != null && val.isNotEmpty) setFilter('country', val);
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
