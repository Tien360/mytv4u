import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

get_age_code = """
  String? _getAgeRating() {
    if (_tmdbDetails == null) return null;
    
    // TV Shows
    if (_tmdbDetails!['content_ratings'] != null && _tmdbDetails!['content_ratings']['results'] != null) {
      final results = _tmdbDetails!['content_ratings']['results'] as List;
      var usRating = results.firstWhere((r) => r['iso_3166_1'] == 'US', orElse: () => null);
      if (usRating != null && usRating['rating'] != null && usRating['rating'].toString().isNotEmpty) {
        return usRating['rating'].toString();
      }
      for (var r in results) {
        if (r['rating'] != null && r['rating'].toString().isNotEmpty) return r['rating'].toString();
      }
    }
    
    // Movies
    if (_tmdbDetails!['release_dates'] != null && _tmdbDetails!['release_dates']['results'] != null) {
      final results = _tmdbDetails!['release_dates']['results'] as List;
      var usRating = results.firstWhere((r) => r['iso_3166_1'] == 'US', orElse: () => null);
      if (usRating != null && usRating['release_dates'] != null) {
        for (var d in usRating['release_dates']) {
          if (d['certification'] != null && d['certification'].toString().isNotEmpty) return d['certification'].toString();
        }
      }
      for (var r in results) {
        if (r['release_dates'] != null) {
          for (var d in r['release_dates']) {
             if (d['certification'] != null && d['certification'].toString().isNotEmpty) return d['certification'].toString();
          }
        }
      }
    }
    return null;
  }
"""

# Insert _getAgeRating
if "_getAgeRating" not in content:
    content = content.replace("Widget _buildBadge(String text, Color color) {", get_age_code + "\n  Widget _buildBadge(String text, Color color) {")

# Render it and the quality tag
old_badges = """                                              if (_premiumServers.isNotEmpty)
                                                _buildBadge(
                                                  'Premium TM - Vietsub',
                                                  Colors.blueAccent,
                                                ),"""

new_badges = """                                              if (_premiumServers.isNotEmpty)
                                                _buildBadge(
                                                  'Premium TM - Vietsub',
                                                  Colors.blueAccent,
                                                ),
                                              if (_movie!.quality.isNotEmpty)
                                                _buildBadge(
                                                  _movie!.quality,
                                                  Colors.greenAccent,
                                                ),
                                              if (_getAgeRating() != null)
                                                _buildBadge(
                                                  _getAgeRating()!,
                                                  ['R', 'NC-17', 'TV-MA', '18+'].contains(_getAgeRating()) ? Colors.redAccent : Colors.orangeAccent,
                                                ),"""

content = content.replace(old_badges, new_badges)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added Age Rating and Quality badges")
