import 'dart:async';
import 'package:flutter/material.dart';
import '../api/phim_api.dart';
import '../models/movie.dart';
import 'movie_detail_screen.dart';
import '../widgets/hover_movie_card.dart';
import '../utils/l10n.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => SearchScreenState();
}

class SearchScreenState extends State<SearchScreen> {
  List<Movie> _movies = [];
  bool _isLoading = false;
  Timer? _debounce;
  String _lastQuery = '';

  void performSearch(String query) {
    if (_lastQuery == query) return;
    _lastQuery = query;

    if (_debounce?.isActive ?? false) _debounce!.cancel();
    if (query.isEmpty) {
      setState(() {
        _movies = [];
        _isLoading = false;
      });
      return;
    }
    
    _debounce = Timer(const Duration(milliseconds: 500), () async {
      setState(() => _isLoading = true);
      final results = await PhimApi.searchMovies(query);
      if (mounted) {
        setState(() {
          _movies = results;
          _isLoading = false;
        });
      }
    });
  }

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return _isLoading
        ? Center(child: CircularProgressIndicator())
        : _movies.isEmpty && _lastQuery.isNotEmpty
            ? Center(child: Text(L10n.t('search_no_results'), style: const TextStyle(color: Colors.white, fontSize: 16)))
            : GridView.builder(
                padding: const EdgeInsets.all(24),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 5,
                  childAspectRatio: 0.65,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                ),
                itemCount: _movies.length,
                itemBuilder: (context, index) {
                  final movie = _movies[index];
                  return HoverMovieCard(
                    movie: movie,
                    heroTag: 'search_${movie.slug}',
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => MovieDetailScreen(slug: movie.slug, heroTag: 'search_${movie.slug}', initialMovie: movie)),
                      );
                    },
                  );
                },
              );
  }
}
