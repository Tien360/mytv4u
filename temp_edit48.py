import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'\n\s*Future<void> _loadEpisodeProgressAndColor\(\) async \{\n\s*// No longer using PaletteGenerator to extract color\.\n\s*// Default color is already Colors\.redAccent\.\n\s*\} catch \(e\) \{\}\n\s*\}\n\s*\}',
    r'''
  Future<void> _loadEpisodeProgressAndColor() async {
    // No longer using PaletteGenerator to extract color.
    // Default color is already Colors.redAccent.
  }''',
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Cleaned up syntax")
