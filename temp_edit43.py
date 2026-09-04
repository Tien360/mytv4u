import sys
import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Find the _loadEpisodeProgressAndColor method
match = re.search(r'(Future<void> _loadEpisodeProgressAndColor\(\) async \{.*?\n  \})', c, re.DOTALL)
if match:
    old_func = match.group(1)
    new_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;

    // Load color in the background
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
    print("Removed heavy loop from _loadEpisodeProgressAndColor")
else:
    print("Could not find _loadEpisodeProgressAndColor")
