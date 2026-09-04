with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# 1. Imports
if "import 'package:palette_generator/palette_generator.dart';" not in c:
    c = c.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:palette_generator/palette_generator.dart';\nimport 'package:cached_network_image/cached_network_image.dart';")

# 2. State variables
state_vars = """
  Color _dominantColor = Colors.redAccent;
  final Map<String, double> _episodeProgressMap = {};

  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie != null && _movie!.thumbUrl.isNotEmpty) {
      try {
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );
        if (mounted) {
          setState(() {
            _dominantColor = paletteGenerator.dominantColor?.color ?? 
                             paletteGenerator.vibrantColor?.color ?? 
                             Colors.redAccent;
          });
        }
      } catch (e) {
        // Fallback color
      }
    }

    if (_movie == null) return;
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final prefix = 'continue_${_movie!.name}_';
    final durationPrefix = 'continue_duration_${_movie!.name}_';

    if (mounted) {
      setState(() {
        for (var key in keys) {
          if (key.startswith(prefix)) {
            final epName = key.substring(prefix.length);
            final posMs = prefs.getInt(key) ?? 0;
            final durKey = durationPrefix + epName;
            final durMs = prefs.getInt(durKey) ?? 0;
            
            if (durMs > 0 && posMs > 0) {
              final double fraction = (posMs / durMs).clamp(0.0, 1.0);
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }
  }
"""
c = c.replace("class _MovieDetailScreenState extends State<MovieDetailScreen> {", "class _MovieDetailScreenState extends State<MovieDetailScreen> {" + state_vars)

# 3. Call in _fetchDetail
fetch_call = """              setState(() {
                _movie = movie;
                _isLoading = false;
              });
              _loadEpisodeProgressAndColor();"""
c = c.replace("""              setState(() {
                _movie = movie;
                _isLoading = false;
              });""", fetch_call)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated movie_detail_screen.dart states")
