import sys

path = r"T:\Project\Phim\mytv4u_flutter\lib\api\phim_api.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find getTrailerStreamUrl start
start_idx = -1
for i, line in enumerate(lines):
    if "static Future<String?> getTrailerStreamUrl(" in line:
        start_idx = i
        break

end_idx = -1
for i in range(start_idx, len(lines)):
    if "static Future<Map<String, dynamic>?> getActorDetails" in lines[i]:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_func = """  static Future<String?> getTrailerStreamUrl(Movie movie, bool isTvSeries) async {
    try {
      String? tmdbId;
      String type = isTvSeries ? 'tv' : 'movie';

      if (movie.imdbId != null && movie.imdbId != '' && movie.imdbId != 'N/A') {
        final findUrl = 'https://api.themoviedb.org/3/find/${movie.imdbId}?external_source=imdb_id&api_key=$_tmdbApiKey';
        final findRes = await http.get(Uri.parse(findUrl)).timeout(const Duration(seconds: 10));
        if (findRes.statusCode == 200) {
          final findData = json.decode(findRes.body);
          if (findData['movie_results'] != null && findData['movie_results'].isNotEmpty) {
            tmdbId = findData['movie_results'][0]['id'].toString();
            type = 'movie';
          } else if (findData['tv_results'] != null && findData['tv_results'].isNotEmpty) {
            tmdbId = findData['tv_results'][0]['id'].toString();
            type = 'tv';
          }
        }
      }

      if (tmdbId == null) {
        final match = await _searchTmdb(movie.name, movie.originalName, movie.year, isTvSeries);
        if (match != null && match['id'] != null) {
          tmdbId = match['id'].toString();
          type = match['type'] ?? type;
        }
      }

      if (tmdbId != null) {
        final videoUrl = 'https://api.themoviedb.org/3/$type/$tmdbId/videos?api_key=$_tmdbApiKey&language=vi-VN&include_video_language=vi,en,null';
        final videoRes = await http.get(Uri.parse(videoUrl));
        if (videoRes.statusCode == 200) {
          final videoData = json.decode(videoRes.body);
          if (videoData['results'] != null && videoData['results'].isNotEmpty) {
            final List results = videoData['results'];
            var trailer = results.firstWhere(
              (v) => v['site'] == 'YouTube' && v['type'] == 'Trailer',
              orElse: () => null,
            );
            trailer ??= results.firstWhere(
              (v) => v['site'] == 'YouTube',
              orElse: () => null,
            );

            if (trailer != null) {
              return trailer['key'];
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi TMDB getTrailerStreamUrl error: $e');
    }

    try {
      final query = Uri.encodeComponent('${movie.originalName} trailer');
      final ytUrl = Uri.parse(
        'https://www.youtube.com/results?search_query=$query',
      );
      final ytRes = await http.get(
        ytUrl,
        headers: {
          'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
      );

      if (ytRes.statusCode == 200) {
        final html = ytRes.body;
        int startIndex = html.indexOf('var ytInitialData = {');
        if (startIndex != -1) {
          int endIndex = html.indexOf(';</script>', startIndex);
          if (endIndex != -1) {
            String jsonStr = html.substring(startIndex + 20, endIndex);
            try {
              final data = json.decode(jsonStr);
              final contents = data['contents']?['twoColumnSearchResultsRenderer']?['primaryContents']?['sectionListRenderer']?['contents'] as List?;
              if (contents != null) {
                for (var section in contents) {
                  if (section['itemSectionRenderer'] != null) {
                    final items = section['itemSectionRenderer']['contents'] as List?;
                    if (items != null) {
                      for (var item in items) {
                        if (item['videoRenderer'] != null) {
                          return item['videoRenderer']['videoId'];
                        }
                      }
                    }
                  }
                }
              }
            } catch (e) {
              print('JSON parse error ytInitialData: $e');
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi YouTube scrape error: $e');
    }

    return null;
  }
"""
    lines[start_idx:end_idx] = [new_func + "\n"]
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully replaced lines", start_idx, "to", end_idx)
else:
    print("Could not find start or end")

