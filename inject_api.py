import re
with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

new_method = """
  static Future<Map<String, dynamic>?> getTmdbFullDetails(
      String title, String originalTitle, String year, bool isTvSeries, String lang) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final tmdbId = match['id'];
        final type = match['type'];

        final url =
            'https://api.themoviedb.org/3/$type/$tmdbId?api_key=$_tmdbApiKey&append_to_response=recommendations,similar,credits&language=$lang';
        final res = await http.get(Uri.parse(url));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);

          if (type == 'movie' && data['belongs_to_collection'] != null) {
            final collectionId = data['belongs_to_collection']['id'];
            final collectionUrl =
                'https://api.themoviedb.org/3/collection/$collectionId?api_key=$_tmdbApiKey&language=$lang';
            final collectionRes = await http.get(Uri.parse(collectionUrl));
            if (collectionRes.statusCode == 200) {
              data['collection_details'] = json.decode(collectionRes.body);
            }
          }
          return data;
        }
      }
    } catch (e) {
      print('PhimApi getTmdbFullDetails error: $e');
    }
    return null;
  }
"""

# Insert new_method before static Future<List<Map<String, String>>> getMovieActors
pattern = r"(\s+static Future<List<Map<String, String>>> getMovieActors)"
new_content = re.sub(pattern, new_method + r"\1", content, count=1)

if new_content != content:
    with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Injected getTmdbFullDetails successfully.")
else:
    print("Could not find getMovieActors.")
