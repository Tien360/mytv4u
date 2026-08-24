import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add _tmdbDetails variable
content = content.replace("List<Map<String, String>> _actors = [];", "List<Map<String, String>> _actors = [];\n  Map<String, dynamic>? _tmdbDetails;")

# Update _fetchTmdbRating and others to use a single fetch
new_fetch = """
  Future<void> _fetchTmdbDetails(Movie movie) async {
    final isTvSeries = movie.episodes.isNotEmpty && movie.episodes.first.items.length > 1;
    final details = await PhimApi.getTmdbFullDetails(
      movie.name,
      movie.originalName,
      movie.year,
      isTvSeries,
      L10n.currentLang == 'vi' ? 'vi-VN' : 'en-US',
    );

    if (mounted && details != null) {
      setState(() {
        _tmdbDetails = details;
        if (details['credits'] != null && details['credits']['cast'] != null) {
           final casts = details['credits']['cast'] as List;
           _actors = casts.take(15).map((c) => {
              'id': c['id']?.toString() ?? '',
              'name': c['name']?.toString() ?? '',
              'character': c['character']?.toString() ?? '',
              'profile_path': c['profile_path']?.toString() ?? '',
           }).toList();
        }
        if (details['vote_average'] != null && details['vote_average'] > 0) {
           _tmdbRating = (details['vote_average'] as num).toDouble();
        }
      });
    } else if (mounted) {
       _fetchActors(movie);
       _fetchTmdbRating(movie);
    }
  }
"""

content = content.replace("Future<void> _fetchActors(Movie m) async {", new_fetch + "\n  Future<void> _fetchActors(Movie m) async {")

# Find the initialization section to call _fetchTmdbDetails
init_pattern = r"if \(_actors\.isEmpty\) \{\s*_fetchActors\(movie\);\s*\}"
content = re.sub(init_pattern, "if (_actors.isEmpty) {\n                  _fetchTmdbDetails(movie);\n                }", content)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated API calls in movie_detail_screen")
