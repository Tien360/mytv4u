import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/movie.dart';

class Film4kNetApi {
  static const String baseUrl = 'https://film4k.net/api';

  static Movie normalize(Map<String, dynamic> item) {
    final titleObj = item['title'] ?? {};
    final title = titleObj['vi'] ?? titleObj['en'] ?? '';
    final originalName = titleObj['en'] ?? title;
    
    final posterObj = item['poster'] ?? {};
    final poster = posterObj['vi'] ?? posterObj['en'] ?? '';
    
    final backdrop = item['backdrop'] ?? '';
    final overviewObj = item['overview'] ?? {};
    final overview = overviewObj['vi'] ?? overviewObj['en'] ?? '';

    final genresObj = item['genres'] ?? {};
    final genresList = genresObj['vi'] ?? genresObj['en'] ?? [];
    
    return Movie(
      name: title,
      originalName: originalName,
      slug: item['slug'] ?? '',
      type: item['mediaType'] == 'tv' ? 'series' : 'single',
      sourceSlugs: {'film4knet': item['slug'] ?? ''},
      thumbUrl: backdrop,
      posterUrl: poster,
      currentEpisode: '',
      quality: 'HD',
      language: 'Vietsub',
      year: (item['year'] ?? '').toString(),
      time: '',
      description: overview,
      genres: (genresList as List).map((e) => e.toString()).toList(),
      countries: [],
      directors: [],
      casts: [],
      episodes: [],
      source: 'film4knet',
    );
  }

  static Future<List<Movie>> getRecent(int page) async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/home?page=$page'));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final list = data['list'] as List? ?? [];
        return list.map((e) => normalize(e as Map<String, dynamic>)).toList();
      }
    } catch (_) {}
    return [];
  }

  static Future<List<Movie>> search(String keyword) async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/home?q=${Uri.encodeComponent(keyword)}'));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final list = data['list'] as List? ?? [];
        return list.map((e) => normalize(e as Map<String, dynamic>)).toList();
      }
    } catch (_) {}
    return [];
  }

  static Future<Movie?> getDetail(String slug) async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/title/$slug'));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final movieData = data['movie'] ?? {};
        var movie = normalize(movieData);

        // Parse episodes
        Map<String, List<Episode>> servers = {};
        
        // If single movie, sources are directly in movieData
        if (movieData['sources'] != null) {
          for (var src in movieData['sources']) {
            String serverName = src['label'] ?? 'Film4k';
            if (!servers.containsKey(serverName)) servers[serverName] = [];
            servers[serverName]!.add(Episode(
              name: 'Full',
              slug: 'full',
              m3u8Url: src['url'] ?? '',
              embedUrl: '',
            ));
          }
        }
        
        // If series, sources are in episodes array
        final epsList = data['episodes'] as List? ?? [];
        for (var ep in epsList) {
          String epName = ep['title'] ?? 'Tập ${ep['episode']}';
          final sources = ep['sources'] as List? ?? [];
          for (var src in sources) {
            String serverName = src['label'] ?? 'Film4k';
            if (!servers.containsKey(serverName)) servers[serverName] = [];
            servers[serverName]!.add(Episode(
              name: epName,
              slug: '${ep['season']}-${ep['episode']}',
              m3u8Url: src['url'] ?? '',
              embedUrl: '',
            ));
          }
        }

        final episodeServers = servers.entries.map((e) => EpisodeServer(
          serverName: e.key,
          items: e.value,
        )).toList();

        return movie.copyWith(episodes: episodeServers);
      }
    } catch (_) {}
    return null;
  }
}
