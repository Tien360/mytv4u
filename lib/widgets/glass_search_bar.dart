import 'package:flutter/material.dart';
import 'glass_container.dart';
import '../screens/movie_detail_screen.dart';
import '../api/phim_api.dart';
import '../models/movie.dart';
import '../utils/ui_utils.dart';
import '../utils/l10n.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class GlassSearchBar extends StatefulWidget {
  final String hintText;
  const GlassSearchBar({super.key, this.hintText = ''});

  @override
  State<GlassSearchBar> createState() => _GlassSearchBarState();
}

class _GlassSearchBarState extends State<GlassSearchBar> {
  final TextEditingController _controller = TextEditingController();
  late stt.SpeechToText _speech;
  bool _isListening = false;

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) {
          if (val == 'done' || val == 'notListening') {
            if (mounted) setState(() => _isListening = false);
            if (_controller.text.isNotEmpty) {
              // _onSearch(_controller.text);
            }
          }
        },
        onError: (val) => print('onError: $val'),
      );
      if (available) {
        setState(() => _isListening = true);

        String locale = L10n.currentLang == 'vi' ? 'vi_VN' : 'en_US';
        _speech.listen(
          localeId: locale,
          onResult: (val) => setState(() {
            _controller.text = val.recognizedWords;
          }),
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      if (_controller.text.isNotEmpty) {
        _onSearch(_controller.text);
      }
    }
  }

  void _onSearch(String query) async {
    if (query.trim().isEmpty) return;

    // Hiện dialog loading
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator()),
    );

    try {
      final results = await PhimApi.searchMovies(query);
      if (mounted) {
        Navigator.pop(context); // Tắt loading
        if (results.isNotEmpty) {
          _showQuickResults(results);
        } else {
          UIUtils.showCustomSnackBar(context, L10n.t('search_no_results'));
        }
      }
    } catch (e) {
      if (mounted) {
        Navigator.pop(context);
        UIUtils.showCustomSnackBar(context, '\: $e', isError: true);
      }
    }
  }

  void _showQuickResults(List<Movie> results) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) {
        return GlassContainer(
          height: MediaQuery.of(context).size.height * 0.7,
          borderRadius: 24,
          child: Column(
            children: [
              const SizedBox(height: 12),
              Container(
                width: 40,
                height: 5,
                decoration: BoxDecoration(
                  color: Colors.white30,
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                L10n.t('search_results'),
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: ListView.builder(
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final movie = results[index];
                    return ListTile(
                      leading: Image.network(
                        movie.thumbUrl,
                        width: 50,
                        height: 75,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) =>
                            const Icon(Icons.movie, color: Colors.white54),
                      ),
                      title: Text(
                        movie.displayName,
                        style: const TextStyle(color: Colors.white),
                      ),
                      subtitle: Text(
                        movie.originalName,
                        style: const TextStyle(color: Colors.white54),
                      ),
                      onTap: () {
                        Navigator.pop(context);
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => MovieDetailScreen(
                              slug: movie.slug,
                              initialMovie: movie,
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return GlassContainer(
      margin: const EdgeInsets.only(left: 16, right: 16, top: 44, bottom: 12),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      height: 48,
      borderRadius: 24,
      color: const Color(0x1A000000), // Glass tối nhẹ
      borderColor: const Color(0x33FFFFFF), // Viền sáng
      blur: 20,
      child: Row(
        children: [
          const Icon(Icons.search, color: Colors.white70),
          const SizedBox(width: 12),
          Expanded(
            child: TextField(
              controller: _controller,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: widget.hintText.isEmpty
                    ? L10n.t('search_hint')
                    : widget.hintText,
                hintStyle: const TextStyle(color: Colors.white38),
                border: InputBorder.none,
              ),
              onSubmitted: _onSearch,
            ),
          ),
          IconButton(
            icon: Icon(
              _isListening ? Icons.mic : Icons.mic_none,
              color: _isListening ? Colors.redAccent : Colors.white70,
            ),
            onPressed: _listen,
            tooltip: 'Tìm kiếm bằng giọng nói',
          ),
        ],
      ),
    );
  }
}
