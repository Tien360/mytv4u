import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;
    
    // 1. Load progress instantly so it doesn't wait for image parsing
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final targetPrefix = 'continue_${_movie!.name.trim()}_'.toLowerCase();

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

new_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;
    
    // 1. Load progress instantly so it doesn't wait for image parsing
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    
    // Robust normalization: lowercase and remove all spaces
    final normalizedMovieName = _movie!.name.toLowerCase().replaceAll(' ', '');
    final targetPrefix = 'continue_${normalizedMovieName}_';

    if (mounted) {
      setState(() {
        for (var key in keys) {
          final normalizedKey = key.toLowerCase().replaceAll(' ', '');
          if (normalizedKey.startsWith(targetPrefix)) {
            // We need to extract the original epName.
            // Since we stripped spaces, we can't just substring the original key safely
            // unless we know exactly where the prefix ends in the original key.
            // A safer way: The original key starts with "continue_" + some variant of movie name + "_" + epName
            // Let's split by "_"
            // "continue_Spider Man_Tập 1" -> parts: ["continue", "Spider Man", "Tập 1"]
            // This is tricky if movie name has underscores!
            
            // Alternative: find the exact index in the original string by matching non-space characters
            int originalIndex = 0;
            int normalizedMatched = 0;
            while (normalizedMatched < targetPrefix.length && originalIndex < key.length) {
                if (key[originalIndex] == ' ') {
                    originalIndex++;
                } else if (key[originalIndex].toLowerCase() == targetPrefix[normalizedMatched]) {
                    originalIndex++;
                    normalizedMatched++;
                } else {
                    break;
                }
            }
            
            final epName = key.substring(originalIndex);
            final posMs = prefs.getInt(key) ?? 0;
            
            int durMs = 0;
            final targetDurPrefix = 'continue_duration_${normalizedMovieName}_' + epName.toLowerCase().replaceAll(' ', '');
            for (var dKey in keys) {
               if (dKey.toLowerCase().replaceAll(' ', '') == targetDurPrefix) {
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
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }"""

c = c.replace(old_func, new_func)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated robust key matching")
