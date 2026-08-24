import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# We want to add _updateAmbientBackground(); right after _currentHeroIndex = ...
content = re.sub(
    r"(_currentHeroIndex\s*=\s*[^;]+;)",
    r"\1\n              _updateAmbientBackground();",
    content
)

# And in _loadHeroMovies:
content = re.sub(
    r"(_isLoadingHero = false;\n\s*})\);",
    r"_isLoadingHero = false;\n        _updateAmbientBackground();\n      });",
    content
)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
