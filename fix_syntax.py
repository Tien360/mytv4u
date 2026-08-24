import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: _tmdbRating assignment
content = content.replace(
    "_tmdbRating = (details['vote_average'] as num).toDouble();",
    "_tmdbRating = (details['vote_average'] as num).toStringAsFixed(1);"
)

# Fix 2: MovieDetailScreen instantiation
content = content.replace(
    "MovieDetailScreen(initialMovie: bestMatch)",
    "MovieDetailScreen(slug: bestMatch.slug, initialMovie: bestMatch)"
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed syntax errors")
