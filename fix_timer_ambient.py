import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix all setState occurrences related to _currentHeroIndex changing
content = re.sub(
    r"_currentHeroIndex = \(_currentHeroIndex \+ 1\) % _heroMovies\.length;\s*\}\);",
    r"_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;\n          _updateAmbientBackground();\n        });",
    content
)

content = re.sub(
    r"_currentHeroIndex =\n\s*\(_currentHeroIndex - 1 \+ _heroMovies\.length\) %\n\s*_heroMovies\.length;\s*\}\);",
    r"_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;\n                _updateAmbientBackground();\n              });",
    content
)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
