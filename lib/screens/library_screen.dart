import 'player_screen.dart';
import 'package:file_picker/file_picker.dart';
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
              padding: const EdgeInsets.only(
                left: 24,
                right: 24,
                top: 24,
                bottom: 16,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    L10n.t('favorite_list') != null &&
                            L10n.t('favorite_list').isNotEmpty
                        ? L10n.t('favorite_list')
                        : 'Thư viện & Yêu thích',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  
                  Row(
                    children: [
                      ElevatedButton.icon(
                        icon: const Icon(Icons.link, color: Colors.white),
                        label: const Text(
                          'Mở Link',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white.withAlpha(25),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 14,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                        ),
                        onPressed: () {
                          _showOpenUrlDialog(context);
                        },
                      ),
                      const SizedBox(width: 12),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.folder_open, color: Colors.white),
                        label: const Text(
                          'Mở File',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white.withAlpha(25),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 14,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                        ),
                        onPressed: () async {

                      try {
                        var files = await FilePicker.pickFiles(
                          type: FileType.custom,
                          allowedExtensions: [
                            
                            'mp4',
                            'mkv',
                            'avi',
                            'flv',
                            'webm',
                            'mov',
                            'ts',
                            'mp3',
                            'm4a',
                            'wav',
                            'flac',
                            'aac',

                          ],
                          allowMultiple: false,
                        );
                        if (files != null &&
                            files.isNotEmpty &&
                            files.single.path != null) {
                          String path = files.single.path!;
                          String filename = files.single.name;
                          String fileUrl =
                              "file:///" + path.replaceAll(r'\\', '/');

                          if (context.mounted) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => PlayerScreen(
                                  episodes: [
                                    Episode(
                                      name: 'Full',
                                      slug: 'full',
                                      m3u8Url: fileUrl,
                                      embedUrl: '',
                                    ),
                                  ],
                                  currentEpisodeIndex: 0,
                                  movieName: filename,
                                ),
                              ),
                            );
                          }
                        }
                      
                      } catch (e) {
                        print("File picker error: " + e.toString());
                      }
                    },
                  ),
                  ],
                  ),

                ],
              ),
            ),

            Expanded(
              child: _isLoading
                  ? Center(child: CircularProgressIndicator())
                  : _watchlist.isEmpty
                  ? Center(
                      child: Text(
                        L10n.t('favorite_empty'),
                        style: const TextStyle(
                          color: Colors.white54,
                          fontSize: 16,
                        ),
                      ),
                    )
                  : GridView.builder(
                      padding: const EdgeInsets.all(16),
                      gridDelegate:
                          const SliverGridDelegateWithFixedCrossAxisCount(
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
                                  icon: const Icon(
                                    Icons.delete_outline,
                                    color: Colors.white,
                                    size: 20,
                                  ),
                                  onPressed: () =>
                                      _removeFromWatchlist(movie.slug),
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

  void _showOpenUrlDialog(BuildContext context) {
    final TextEditingController _urlController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2C),
        title: const Text('Mở đường dẫn mạng (URL)', style: TextStyle(color: Colors.white)),
        content: TextField(
          controller: _urlController,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Nhập link video/audio (mp4, m3u8, mp3...)',
            hintStyle: TextStyle(color: Colors.white54),
            enabledBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.white24),
            ),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.blueAccent),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Hủy', style: TextStyle(color: Colors.white54)),
          ),
          ElevatedButton(
            onPressed: () {
              final url = _urlController.text.trim();
              if (url.isNotEmpty) {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => PlayerScreen(
                      episodes: [
                        Episode(
                          name: 'Stream',
                          slug: 'stream',
                          m3u8Url: url,
                          embedUrl: '',
                        ),
                      ],
                      currentEpisodeIndex: 0,
                      movieName: 'Network Stream',
                    ),
                  ),
                );
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
            child: const Text('Mở', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
