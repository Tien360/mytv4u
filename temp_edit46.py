import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_func = """  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;

    // Load color in the background
    if (_movie!.thumbUrl.isNotEmpty) {
      try {
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );"""

new_func = """  bool _hasComputedColor = false;
  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie == null) return;

    // Load color in the background ONLY ONCE per movie
    if (_movie!.thumbUrl.isNotEmpty && !_hasComputedColor) {
      try {
        _hasComputedColor = true;
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );"""

c = c.replace(old_func, new_func)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Prevented PaletteGenerator from running multiple times")
