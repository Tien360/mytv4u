import sys

code = """import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../widgets/glass_container.dart';
import '../utils/l10n.dart';
import 'game_detail_screen.dart';

class GamingScreen extends StatefulWidget {
  const GamingScreen({Key? key}) : super(key: key);

  @override
  State<GamingScreen> createState() => _GamingScreenState();
}

class _GamingScreenState extends State<GamingScreen> {
  final List<Map<String, String>> _games = [
    {
      'title': 'Stealth Master',
      'url': 'https://www.youtube.com/playables/UgkxAa2Gygx3bQRx4kOraVwUFW_3mO1tH0h5',
      'image': 'https://img.utdstc.com/icon/e19/39f/e1939faab6c7d1f1f1e53674c5b703f69c75ff345494a3c55b1d60e9f7014fdf:600',
    }
  ];

  void _onGameTap(String url, String title, String image) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GameDetailScreen(
          gameUrl: url,
          gameTitle: title,
          initialThumb: image,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            L10n.t('nav_gaming') ?? 'Trò chơi (YouTube Playables)',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.0,
              ),
              itemCount: _games.length,
              itemBuilder: (context, index) {
                final game = _games[index];
                return _GameCard(
                  game: game,
                  onTap: () => _onGameTap(game['url']!, game['title']!, game['image']!),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _GameCard extends StatefulWidget {
  final Map<String, String> game;
  final VoidCallback onTap;
  
  const _GameCard({Key? key, required this.game, required this.onTap}) : super(key: key);

  @override
  State<_GameCard> createState() => _GameCardState();
}

class _GameCardState extends State<_GameCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: AnimatedScale(
          scale: _isHovered ? 1.05 : 1.0,
          duration: const Duration(milliseconds: 200),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              boxShadow: _isHovered
                  ? [BoxShadow(color: Colors.blueAccent.withOpacity(0.5), blurRadius: 15, spreadRadius: 2)]
                  : [],
            ),
            child: GlassContainer(
              borderRadius: 16,
              padding: const EdgeInsets.all(0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                      child: CachedNetworkImage(
                        imageUrl: widget.game['image']!,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(12),
                    color: _isHovered ? Colors.blueAccent.withOpacity(0.8) : Colors.black45,
                    child: Text(
                      widget.game['title']!,
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
"""
with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated gaming_screen.dart")
