import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# The incorrect part starts from:
# 'https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=import \'dart:async\';

# It goes all the way to:
#     print('PhimApi TMDB getMovieTmdbLogo error: import \'dart:async\';

# We can just extract the bad block using regex or string manipulation.
# Since it's easiest to just rebuild `getMovieTmdbLogo`:

# First, find where getMovieTmdbLogo starts
start_idx = content.find("  static Future<String?> getMovieTmdbLogo(")
# find where getMovieTmdbBackdrop starts
end_idx = content.find("  static Future<String?> getMovieTmdbBackdrop(")

if start_idx != -1 and end_idx != -1:
    correct_method = """  static Future<String?> getMovieTmdbLogo(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
    String language,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final imgUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=$_tmdbApiKey';
        final res = await http.get(Uri.parse(imgUrl));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          if (data['logos'] != null && (data['logos'] as List).isNotEmpty) {
            final List logos = data['logos'];
            var targetLogo = logos.firstWhere(
                (l) => l['iso_639_1'] == language,
                orElse: () => null);
            if (targetLogo != null) {
              return 'https://image.tmdb.org/t/p/w500${targetLogo['file_path']}';
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi TMDB getMovieTmdbLogo error: $e');
    }
    return null;
  }

"""
    new_content = content[:start_idx] + correct_method + content[end_idx:]
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed!")
else:
    print("Could not find start or end index.")
