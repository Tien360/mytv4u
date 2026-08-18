import 'package:flutter/material.dart';
import '../api/firebase_api.dart';
import '../models/movie.dart';
import '../utils/ui_utils.dart';
import '../utils/l10n.dart';
import 'movie_detail_screen.dart';
import '../widgets/hover_movie_card.dart';

class LibraryScreen extends StatefulWidget {
  const LibraryScreen({super.key});

  @override
  State<LibraryScreen> createState() => LibraryScreenState();
}

class LibraryScreenState extends State<LibraryScreen> {
  List<Map<String, dynamic>> _watchlist = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchWatchlist();
  }

  Future<void> _fetchWatchlist() async {
    setState(() => _isLoading = true);
    final list = await FirebaseApi.getWatchlist();
    if (mounted) {
      setState(() {
        _watchlist = list;
        _isLoading = false;
      });
    }
  }

  void refresh() {
    _fetchWatchlist();
  }

  Future<void> _removeFromWatchlist(String slug) async {
    await FirebaseApi.removeFromWatchlist(slug);
    UIUtils.showCustomSnackBar(context, L10n.t('removed_favorite'));
    _fetchWatchlist();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        top: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(left: 24, top: 24, bottom: 16),
              child: Text(
                L10n.t('favorite_list'),
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Expanded(
              child: _isLoading
                  ? Center(child: CircularProgressIndicator())
                  : _watchlist.isEmpty
                      ? Center(
                          child: Text(
                            L10n.t('favorite_empty'),
                            style: const TextStyle(color: Colors.white54, fontSize: 16),
                          ),
                        )
                      : GridView.builder(
                          padding: const EdgeInsets.all(16),
                          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 5,
                            childAspectRatio: 0.65,
                            crossAxisSpacing: 16,
                            mainAxisSpacing: 16,
                          ),
                          itemCount: _watchlist.length,
                          itemBuilder: (context, index) {
                            final item = _watchlist[index];
                            final movie = Movie(
                              name: item['name'] ?? '',
                              originalName: '',
                              slug: item['slug'] ?? '',
                              thumbUrl: item['thumbUrl'] ?? '',
                              posterUrl: '',
                              currentEpisode: '',
                              quality: '',
                              language: '',
                              year: '2024',
                              time: '',
                              description: '',
                              genres: [],
                              countries: [],
                              directors: [],
                              casts: [],
                              episodes: [],
                              source: item['source'] ?? 'nguonc',
                            );
                            
                            return Stack(
                              children: [
                                HoverMovieCard(
                                  movie: movie,
                                  heroTag: 'watchlist_${movie.slug}',
                                  onTap: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => MovieDetailScreen(
                                          slug: movie.slug,
                                          initialMovie: movie,
                                          heroTag: 'watchlist_${movie.slug}',
                                        ),
                                      ),
                                    ).then((_) {
                                      // Cập nhật lại list sau khi trở về từ Detail
                                      _fetchWatchlist();
                                    });
                                  },
                                ),
                                Positioned(
                                  top: 8,
                                  right: 8,
                                  child: Material(
                                    color: Colors.black.withOpacity(0.6),
                                    shape: const CircleBorder(),
                                    child: IconButton(
                                      icon: const Icon(Icons.delete_outline, color: Colors.white, size: 20),
                                      onPressed: () => _removeFromWatchlist(movie.slug),
                                      tooltip: L10n.t('remove_favorite'),
                                    ),
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }
}
