import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/movie.dart';

class CinemetaApi {
  static const String _baseUrl = 'https://v3-cinemeta.strem.io';

  /// Fetch TV series metadata to get seasons and episodes
  static Future<List<Map<String, dynamic>>> getSeriesEpisodes(String imdbId) async {
    try {
      final url = '$_baseUrl/meta/series/$imdbId.json';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode != 200) return [];
      final data = json.decode(res.body);
      final meta = data['meta'] as Map<String, dynamic>?;
      if (meta == null) return [];
      final videos = meta['videos'] as List<dynamic>?;
      if (videos == null) return [];
      return videos.map((v) => v as Map<String, dynamic>).toList();
    } catch (e) {
      print('CinemetaApi getSeriesEpisodes error: $e');
      return [];
    }
  }

  static Movie _parseToMovie(Map<String, dynamic> item) {
    String name = (item['name'] ?? '').toString();
    String imdbId = (item['imdb_id'] ?? '').toString();
    String type = (item['type'] ?? '').toString();
    String posterUrl = (item['poster'] ?? '').toString();
    String backgroundUrl = (item['background'] ?? '').toString();
    String year = (item['year'] ?? '').toString();
    if (year.contains('-')) {
        year = year.split('-')[0];
    }

    String desc = (item['description'] ?? '').toString();
    String runtime = (item['runtime'] ?? '').toString();
    
    List<String> casts = [];
    if (item['cast'] != null && item['cast'] is List) {
        casts = (item['cast'] as List).map((e) => e.toString()).toList();
    }
    List<String> directors = [];
    if (item['director'] != null && item['director'] is List) {
        directors = (item['director'] as List).map((e) => e.toString()).toList();
    }
    List<String> genres = [];
    if (item['genre'] != null && item['genre'] is List) {
        genres = (item['genre'] as List).map((e) => e.toString()).toList();
    }

    return Movie(
      imdbId: imdbId,
      type: type,
      name: name,
      originalName: name, // Cinemeta typically returns original/english name
      slug: imdbId,
      thumbUrl: posterUrl,
      posterUrl: backgroundUrl.isNotEmpty ? backgroundUrl : posterUrl,
      currentEpisode: type == 'series' ? 'Series' : 'Full',
      quality: 'HD',
      language: 'N/A', // Let Vietnamese sources fill this if merged
      year: year,
      time: runtime.isNotEmpty ? runtime : 'N/A',
      description: desc,
      genres: genres,
      countries: [],
      directors: directors,
      casts: casts,
      episodes: [],
      sourceSlugs: {'stremio': imdbId},
      source: 'stremio',
    );
  }

  static Future<List<Movie>> searchCinemeta(String keyword) async {
    try {
      final enc = Uri.encodeComponent(keyword);
      // We can search both movies and series in parallel, or just use movie catalog and it sometimes returns series, but let's query both
      final List<Movie> results = [];
      
      final movieRes = await http.get(Uri.parse('$_baseUrl/catalog/movie/top/search=$enc.json')).timeout(const Duration(seconds: 10));
      if (movieRes.statusCode == 200) {
        final data = json.decode(movieRes.body);
        if (data['metas'] != null) {
          results.addAll((data['metas'] as List).map((e) => _parseToMovie(e)));
        }
      }
      
      final seriesRes = await http.get(Uri.parse('$_baseUrl/catalog/series/top/search=$enc.json')).timeout(const Duration(seconds: 10));
      if (seriesRes.statusCode == 200) {
        final data = json.decode(seriesRes.body);
        if (data['metas'] != null) {
          results.addAll((data['metas'] as List).map((e) => _parseToMovie(e)));
        }
      }
      
      return results;
    } catch (e) {
      print('CinemetaApi search error: $e');
      return [];
    }
  }

  static Future<List<Movie>> getTopMovies() async {
    try {
      final List<Movie> results = [];
      final movieRes = await http.get(Uri.parse('$_baseUrl/catalog/movie/top.json')).timeout(const Duration(seconds: 10));
      if (movieRes.statusCode == 200) {
        final data = json.decode(movieRes.body);
        if (data['metas'] != null) {
          results.addAll((data['metas'] as List).map((e) => _parseToMovie(e)));
        }
      }
      return results;
    } catch (e) {
      print('CinemetaApi top movies error: $e');
      return [];
    }
  }

  static Future<Movie?> getMetaDetail(String imdbId, {bool isSeries = false}) async {
    try {
      final type = isSeries ? 'series' : 'movie';
      final res = await http.get(Uri.parse('$_baseUrl/meta/$type/$imdbId.json')).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        if (data['meta'] != null) {
          return _parseToMovie(data['meta']);
        }
      }
      return null;
    } catch (e) {
      print('CinemetaApi meta detail error: $e');
      return null;
    }
  }
}
