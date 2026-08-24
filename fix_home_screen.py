import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "ambient_background.dart" not in content:
    content = content.replace("import '../widgets/glass_search_bar.dart';", "import '../widgets/glass_search_bar.dart';\nimport '../widgets/ambient_background.dart';")

# Replace _currentHeroIndex = ... with calling a method
# Wait, let's just do a string replace for setState(() { \n _currentHeroIndex = ...; \n });
# Since there are multiple places, maybe just create a setter property or method and replace.

content = content.replace(
"""          setState(() {
            _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
          });""",
"""          setState(() {
            _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
            _updateAmbientBackground();
          });""")

content = content.replace(
"""              setState(() {
                _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
              });""",
"""              setState(() {
                _currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;
                _updateAmbientBackground();
              });""")

content = content.replace(
"""              setState(() {
                _currentHeroIndex =
                    (_currentHeroIndex - 1 + _heroMovies.length) %
                    _heroMovies.length;
              });""",
"""              setState(() {
                _currentHeroIndex =
                    (_currentHeroIndex - 1 + _heroMovies.length) %
                    _heroMovies.length;
                _updateAmbientBackground();
              });""")

content = content.replace(
"""                                          setState(() {
                                            _currentHeroIndex = index;
                                          });""",
"""                                          setState(() {
                                            _currentHeroIndex = index;
                                            _updateAmbientBackground();
                                          });""")

content = content.replace(
"""        _isLoadingHero = false;
      });""",
"""        _isLoadingHero = false;
        _updateAmbientBackground();
      });""")

# Insert _updateAmbientBackground method
if "_updateAmbientBackground()" not in content:
    method = """  void _updateAmbientBackground() {
    if (_heroMovies.isNotEmpty) {
      globalAmbientImageUrl.value = _heroMovies[_currentHeroIndex].posterUrl.isNotEmpty 
          ? _heroMovies[_currentHeroIndex].posterUrl 
          : _heroMovies[_currentHeroIndex].thumbUrl;
    }
  }

  void _startHeroTimer() {"""
    content = content.replace("  void _startHeroTimer() {", method)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
