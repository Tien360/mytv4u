import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add TmdbLogoInfo class
logo_class = '''
class TmdbLogoInfo {
  final String? url;
  final String lang;
  final String tmdbEnName;
  final String tmdbOriginalName;

  TmdbLogoInfo({
    this.url,
    required this.lang,
    required this.tmdbEnName,
    required this.tmdbOriginalName,
  });
}

class PhimApi {'''
content = content.replace('class PhimApi {', logo_class, 1)

# 2. Update _searchTmdb signature
search_tmdb_old = '''  static Future<Map<String, dynamic>?> _searchTmdb(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    String type = isTvSeries ? 'tv' : 'movie';
    final query = Uri.encodeComponent(
      originalTitle.isNotEmpty ? originalTitle : title,
    );
    final searchUrl =
        'https://api.themoviedb.org/3/search/multi?query=$query&api_key=$_tmdbApiKey&language=vi-VN';'''

search_tmdb_new = '''  static Future<Map<String, dynamic>?> _searchTmdb(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries, {
    String language = 'vi-VN',
  }) async {
    String type = isTvSeries ? 'tv' : 'movie';
    final query = Uri.encodeComponent(
      originalTitle.isNotEmpty ? originalTitle : title,
    );
    final searchUrl =
        'https://api.themoviedb.org/3/search/multi?query=$query&api_key=$_tmdbApiKey&language=$language';'''

content = content.replace(search_tmdb_old, search_tmdb_new, 1)

# 3. Update getMovieTmdbLogo
get_logo_old = '''  static Future<String?> getMovieTmdbLogo(
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
  }'''

get_logo_new = '''  static Future<TmdbLogoInfo?> getMovieTmdbLogo(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
    String appLang,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries, language: 'en-US');
      if (match != null && match['id'] != null) {
        String tmdbEnName = match['title'] ?? match['name'] ?? originalTitle;
        String tmdbOriginalName = match['original_title'] ?? match['original_name'] ?? originalTitle;

        final imgUrl = 'https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=$_tmdbApiKey';
        final res = await http.get(Uri.parse(imgUrl));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          if (data['logos'] != null && (data['logos'] as List).isNotEmpty) {
            final List logos = data['logos'];
            
            List<String?> priorities = [];
            if (appLang == 'vi') {
              priorities = ['vi', 'en', 'xx', null, ''];
            } else {
              priorities = ['en', 'xx', null, ''];
            }

            for (String? lang in priorities) {
              var targetLogo = logos.firstWhere(
                  (l) => l['iso_639_1'] == lang,
                  orElse: () => null);
              if (targetLogo != null) {
                return TmdbLogoInfo(
                  url: 'https://image.tmdb.org/t/p/w500${targetLogo['file_path']}',
                  lang: targetLogo['iso_639_1'] ?? 'none',
                  tmdbEnName: tmdbEnName,
                  tmdbOriginalName: tmdbOriginalName,
                );
              }
            }
          }
        }
        
        return TmdbLogoInfo(
          url: null,
          lang: 'none',
          tmdbEnName: tmdbEnName,
          tmdbOriginalName: tmdbOriginalName,
        );
      }
    } catch (e) {
      print('PhimApi TMDB getMovieTmdbLogo error: $e');
    }
    return null;
  }'''

content = content.replace(get_logo_old, get_logo_new, 1)

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)
