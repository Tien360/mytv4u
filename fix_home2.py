import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "ambient_background.dart" not in content:
    content = content.replace("import '../widgets/glass_search_bar.dart';", "import '../widgets/glass_search_bar.dart';\nimport '../widgets/ambient_background.dart';")

# Add method
method = """  void _updateAmbientBackground() {
    if (_heroMovies.isNotEmpty) {
      globalAmbientImageUrl.value = _heroMovies[_currentHeroIndex].posterUrl.isNotEmpty 
          ? _heroMovies[_currentHeroIndex].posterUrl 
          : _heroMovies[_currentHeroIndex].thumbUrl;
    }
  }

  void _startHeroTimer() {"""
content = content.replace("  void _startHeroTimer() {", method)

# Add calls safely
content = content.replace(
    "_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;",
    "_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;\n            _updateAmbientBackground();"
)

content = content.replace(
    "_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;",
    "_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;\n            _updateAmbientBackground();"
)

content = content.replace(
    "_currentHeroIndex = index;",
    "_currentHeroIndex = index;\n                                          _updateAmbientBackground();"
)

content = content.replace(
    "_isLoadingHero = false;",
    "_isLoadingHero = false;\n        _updateAmbientBackground();"
)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
