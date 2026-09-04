import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie != null && _movie!.thumbUrl.isNotEmpty) {
      try {
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );
        if (mounted) {
          setState(() {
            _dominantColor = paletteGenerator.vibrantColor?.color ?? 
                             paletteGenerator.dominantColor?.color ?? 
                             Colors.redAccent;
          });
        }
      } catch (e) {}
    }

    if (_movie == null) return;
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final prefix = 'continue_${_movie!.name}_';
    final durationPrefix = 'continue_duration_${_movie!.name}_';

    if (mounted) {
      setState(() {
        for (var key in keys) {
          if (key.startsWith(prefix)) {
            final epName = key.substring(prefix.length);
            final posMs = prefs.getInt(key) ?? 0;
            final durKey = durationPrefix + epName;
            final durMs = prefs.getInt(durKey) ?? 0;
            
            if (posMs > 0) {
              double fraction = 0.05;
              if (durMs > 0) {
                fraction = (posMs / durMs).clamp(0.0, 1.0);
              }
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }
  }"""

new_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;
    
    // 1. Load progress instantly so it doesn't wait for image parsing
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final prefix = 'continue_${_movie!.name}_';
    final durationPrefix = 'continue_duration_${_movie!.name}_';

    if (mounted) {
      setState(() {
        for (var key in keys) {
          if (key.startsWith(prefix)) {
            final epName = key.substring(prefix.length);
            final posMs = prefs.getInt(key) ?? 0;
            final durKey = durationPrefix + epName;
            final durMs = prefs.getInt(durKey) ?? 0;
            
            if (posMs > 0) {
              double fraction = 0.05;
              if (durMs > 0) {
                fraction = (posMs / durMs).clamp(0.0, 1.0);
              }
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }
    
    // 2. Load color in the background
    if (_movie!.thumbUrl.isNotEmpty) {
      try {
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );
        if (mounted) {
          setState(() {
            _dominantColor = paletteGenerator.vibrantColor?.color ?? 
                             paletteGenerator.dominantColor?.color ?? 
                             Colors.redAccent;
          });
        }
      } catch (e) {}
    }
  }"""

c = c.replace(old_func, new_func)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Swapped order of progress loading and color loading")
