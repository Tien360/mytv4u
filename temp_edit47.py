import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# Find the _loadEpisodeProgressAndColor method and replace it completely
c = re.sub(
    r'bool _hasComputedColor = false;\n\s*Future<void> _loadEpisodeProgressAndColor\(\) async \{[\s\S]*?\}\n\s*\}',
    r'''  Future<void> _loadEpisodeProgressAndColor() async {
    // No longer using PaletteGenerator to extract color.
    // Default color is already Colors.redAccent.
  }''',
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Removed PaletteGenerator completely")
