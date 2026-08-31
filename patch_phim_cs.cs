using System;
using System.IO;
using System.Text.RegularExpressions;

class Program {
    static void Main() {
        string path = @"T:\Project\Phim\mytv4u_flutter\lib\api\phim_api.dart";
        string content = File.ReadAllText(path);
        
        string pattern = @"static Future<String\?> getTrailerStreamUrl\([^)]+\)\s*async\s*\{(?s).*?(?=\s*// Fallback: T[i\?]m ki\?m tr\?c ti\?p tr[e\?]n YouTube)";
        
        string newCode = @"static Future<String?> getTrailerStreamUrl(Movie movie, bool isTvSeries) async {
    try {
      String? tmdbId;
      String type = isTvSeries ? ""tv"" : ""movie"";

      if (movie.imdbId != null && movie.imdbId != """" && movie.imdbId != ""N/A"") {
        final findUrl = $""https://api.themoviedb.org/3/find/{movie.imdbId}?external_source=imdb_id&api_key={_tmdbApiKey}"";
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
        final videoUrl = $""https://api.themoviedb.org/3/{type}/{tmdbId}/videos?api_key={_tmdbApiKey}&language=vi-VN&include_video_language=vi,en,null"";
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
    }";

        content = Regex.Replace(content, pattern, newCode);

        // Also replace the fallback query
        string fallbackPattern = @"final query = Uri\.encodeComponent\('\$originalTitle trailer'\);";
        string newFallback = @"final query = Uri.encodeComponent('${movie.originalName} trailer');";
        content = Regex.Replace(content, fallbackPattern, newFallback);

        File.WriteAllText(path, content);
        Console.WriteLine("Done patching getTrailerStreamUrl!");
    }
}
