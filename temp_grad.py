import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

pattern = r'                            gradient: LinearGradient\(\s*colors: \[\s*Colors\.transparent,\s*Colors\.black\.withValues\(alpha: 0\.4\),\s*Colors\.black\.withValues\(alpha: 0\.85\),\s*Colors\.black,\s*\],\s*begin: Alignment\.topCenter,\s*end: Alignment\.bottomCenter,\s*stops: const \[0\.0, 0\.05, 0\.15, 1\.0\],\s*\),'

new_gradient = """                            gradient: LinearGradient(
                              colors: [
                                Colors.transparent,
                                Colors.black.withValues(alpha: 0.4),
                                Colors.black.withValues(alpha: 0.8),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.15, 0.35, 1.0], // Smoother transition
                            ),"""

c = re.sub(pattern, new_gradient, c, count=1)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Smoothed black gradient")
