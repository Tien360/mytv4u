import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_func = """  Future<void> _loadEpisodeProgressAndColor() async {
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
    }"""

new_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;
    
    // 1. Load progress instantly so it doesn't wait for image parsing
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final targetPrefix = 'continue_${_movie!.name}_'.toLowerCase();

    if (mounted) {
      setState(() {
        for (var key in keys) {
          if (key.toLowerCase().startsWith(targetPrefix)) {
            // Find exact prefix length in the original key by matching case-insensitively
            // Since we know it starts with it, we just take substring
            final epName = key.substring(targetPrefix.length);
            final posMs = prefs.getInt(key) ?? 0;
            
            // Try to find matching duration key (case-insensitive)
            int durMs = 0;
            final targetDurPrefix = 'continue_duration_${_movie!.name}_${epName}'.toLowerCase();
            for (var dKey in keys) {
               if (dKey.toLowerCase() == targetDurPrefix) {
                  durMs = prefs.getInt(dKey) ?? 0;
                  break;
               }
            }
            
            if (posMs > 0) {
              double fraction = 0.05;
              if (durMs > 0) {
                fraction = (posMs / durMs).clamp(0.0, 1.0);
              }
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;
              // Save with standard case so UI can match it
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }"""

c = c.replace(old_func, new_func)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated _loadEpisodeProgressAndColor to use case-insensitive prefix matching")
