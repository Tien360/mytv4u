import io

with open("lib/api/tmdb_api.dart", "r", encoding="utf-8") as f:
    c = f.read()

replacement = """  static Future<List<dynamic>> getSeasonEpisodes(int tmdbId, int seasonNumber, String language) async {
    try {
      final lang = language == 'vi' ? 'vi-VN' : 'en-US';
      final url = '$_baseUrl/tv/$tmdbId/season/$seasonNumber?api_key=$_apiKey&language=$lang';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        final episodes = data['episodes'] as List<dynamic>? ?? [];
        
        if (language == 'vi') {
          bool needsEnglish = episodes.any((ep) => (ep['overview'] == null || ep['overview'].isEmpty) || (ep['name'] == null || ep['name'].isEmpty));
          
          if (needsEnglish) {
            final urlEn = '$_baseUrl/tv/$tmdbId/season/$seasonNumber?api_key=$_apiKey&language=en-US';
            final resEn = await http.get(Uri.parse(urlEn)).timeout(const Duration(seconds: 10));
            if (resEn.statusCode == 200) {
              final dataEn = json.decode(utf8.decode(resEn.bodyBytes));
              final episodesEn = dataEn['episodes'] as List<dynamic>? ?? [];
              
              for (int i = 0; i < episodes.length; i++) {
                if (i < episodesEn.length) {
                  final epVi = episodes[i];
                  final epEn = episodesEn[i];
                  if (epVi['overview'] == null || epVi['overview'].isEmpty) {
                    if (epEn['overview'] != null && epEn['overview'].isNotEmpty) {
                      epVi['overview'] = epEn['overview'];
                      epVi['_needs_translation'] = true;
                    }
                  }
                  if (epVi['name'] == null || epVi['name'].isEmpty) {
                    if (epEn['name'] != null && epEn['name'].isNotEmpty) {
                      epVi['name'] = epEn['name'];
                    }
                  }
                }
              }
            }
          }
        }
        
        return episodes;
      }
    } catch (e) {
      print('Lỗi lấy SeasonEpisodes: $e');
    }
    return [];
  }"""

start_idx = c.find("  static Future<List<dynamic>> getSeasonEpisodes")
c = c[:start_idx] + replacement + "\n}\n"

with open("lib/api/tmdb_api.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated tmdb_api.dart with English fallback")
