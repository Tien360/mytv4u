import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/movie.dart';

class HoverMovieCard extends StatefulWidget {
  final Movie movie;
  final VoidCallback onTap;
  final String? heroTag;

  const HoverMovieCard({
    super.key,
    required this.movie,
    required this.onTap,
    this.heroTag,
  });

  @override
  State<HoverMovieCard> createState() => _HoverMovieCardState();
}

class _HoverMovieCardState extends State<HoverMovieCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: TweenAnimationBuilder<double>(
          tween: Tween<double>(begin: 0.0, end: _isHovered ? 1.0 : 0.0),
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOutBack,
          builder: (context, value, child) {
            return Transform.scale(
              scale: 1.0 + (0.05 * value),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: value > 0 ? [
                    BoxShadow(color: Colors.black45, blurRadius: 15 * value, spreadRadius: 2 * value),
                  ] : null,
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      Hero(
                        tag: widget.heroTag ?? widget.movie.slug,
                        child: CachedNetworkImage(
                          imageUrl: widget.movie.thumbUrl.isNotEmpty ? widget.movie.thumbUrl : 'https://via.placeholder.com/300x450',
                          fit: BoxFit.cover,
                          errorWidget: (context, url, error) => const Icon(Icons.error, color: Colors.white54),
                        ),
                      ),
                      if (_isHovered)
                        Container(
                          color: Colors.black26,
                          child: const Center(
                            child: Icon(Icons.play_circle_fill, size: 48, color: Colors.white70),
                          ),
                        ),
                      if (widget.movie.source == 'premium')
                        Positioned(
                          top: 8,
                          right: 8,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 4),
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(colors: [Colors.amber, Colors.orange]),
                              borderRadius: BorderRadius.circular(4),
                              boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4)],
                            ),
                            child: const Text('PREMIUM', style: TextStyle(color: Colors.black, fontSize: 10, fontWeight: FontWeight.bold)),
                          ),
                        ),
                      // Hiển thị tên phim ở dưới khi hover
                      if (_isHovered)
                        Positioned(
                          bottom: 0, left: 0, right: 0,
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                begin: Alignment.bottomCenter,
                                end: Alignment.topCenter,
                                colors: [Colors.black.withOpacity(0.9), Colors.transparent],
                              ),
                            ),
                            child: Text(
                              widget.movie.name,
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              textAlign: TextAlign.center,
                            ),
                          ),
                        )
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
