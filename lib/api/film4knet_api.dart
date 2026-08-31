import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/movie.dart';
import 'film4k_proxy.dart';

class Film4kNetApi {
  static const String baseUrl = 'https://film4k.net/api';

  static Movie normalize(Map<String, dynamic> item) {
    String title = '';
    String originalName = '';
    
    if (item['title'] is Map) {
      final titleObj = item['title'];
      title = titleObj['vi'] ?? titleObj['en'] ?? '';
      originalName = titleObj['en'] ?? title;
    } else if (item['title'] is String) {
      title = item['title'];
      originalName = item['originalName'] ?? item['original_name'] ?? title;
    }

    String poster = '';
    if (item['poster'] is Map) {
      final posterObj = item['poster'];
      poster = posterObj['vi'] ?? posterObj['en'] ?? '';
    } else if (item['poster'] is String) {
      poster = item['poster'];
    }

    final backdrop = item['backdrop'] ?? '';
    
    String overview = '';
    if (item['overview'] is Map) {
      final overviewObj = item['overview'];
      overview = overviewObj['vi'] ?? overviewObj['en'] ?? '';
    } else if (item['overview'] is String) {
      overview = item['overview'];
    }

    List<String> genresList = [];
    if (item['genres'] is Map) {
      final genresObj = item['genres'];
      final rawGenres = genresObj['vi'] ?? genresObj['en'] ?? [];
      if (rawGenres is List) {
        genresList = rawGenres.map((e) => e.toString()).toList();
      }
    } else if (item['genres'] is List) {
      genresList = (item['genres'] as List).map((e) => e.toString()).toList();
    }

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
      genres: genresList,
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
      final enc = Uri.encodeComponent(keyword).replaceAll('%20', '+');
      final res = await http.get(
        Uri.parse('$baseUrl/home?q=$enc'),
      );
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
      final res = await http.get(Uri.parse('$baseUrl/watch/$slug'));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final movieData = data['movie'] ?? {};
        var movie = normalize(movieData);

        Map<String, List<Episode>> servers = {};

        bool isValidUrl(String url) {
          if (url.isEmpty) return false;
          if (url.startsWith('/')) return true;
          if (url.contains('film4k.net')) return true;
          return false;
        }

        String buildFullUrl(String url) {
          if (url.startsWith('/')) {
            return 'https://film4k.net' + url;
          }
          return url;
        }
        
        bool shouldIgnoreLabel(String label) {
          final lower = label.toLowerCase();
          return lower.contains('kkphim') || 
                 lower.contains('vsmov') || 
                 lower.contains('nguonc') || 
                 lower.contains('ophim');
        }

        final rootSources = data['sources'] as List? ?? [];
        if (rootSources.isNotEmpty) {
          for (var src in rootSources) {
            String url = src['url'] ?? '';
            if (isValidUrl(url)) {
              String rawLabel = src['label'] ?? 'Archive';
              if (shouldIgnoreLabel(rawLabel)) continue;
              String serverName = 'Film4kNet - ' + rawLabel;
              if (!servers.containsKey(serverName)) servers[serverName] = [];
              servers[serverName]!.add(
                Episode(
                  name: 'Full',
                  slug: 'full',
                  m3u8Url: Film4kProxy.processUrl(buildFullUrl(url)),
                  embedUrl: '',
                ),
              );
            }
          }
        } else if (movieData['hlsUrl'] != null && isValidUrl(movieData['hlsUrl'])) {
          String serverName = 'Film4kNet - Archive';
          servers[serverName] = [
            Episode(
              name: 'Full',
              slug: 'full',
              m3u8Url: Film4kProxy.processUrl(buildFullUrl(movieData['hlsUrl'])),
              embedUrl: '',
            ),
          ];
        }

        final epsList = data['episodes'] as List? ?? [];
        for (var ep in epsList) {
          String epName = 'Tập ';
          if (ep['episode'] != null) {
            epName = 'Tập ${ep['episode']}';
          } else if (ep['title'] != null) {
            epName = ep['title'];
          }

          final sources = ep['sources'] as List? ?? [];
          for (var src in sources) {
            String url = src['url'] ?? '';
            if (isValidUrl(url)) {
              String rawLabel = src['label'] ?? 'Archive';
              if (shouldIgnoreLabel(rawLabel)) continue;
              String serverName = 'Film4kNet - ' + rawLabel;
              if (!servers.containsKey(serverName)) servers[serverName] = [];
              servers[serverName]!.add(
                Episode(
                  name: epName,
                  slug: '-',
                  m3u8Url: Film4kProxy.processUrl(buildFullUrl(url)),
                  embedUrl: '',
                ),
              );
            }
          }
        }

        final episodeServers = servers.entries
            .map((e) => EpisodeServer(serverName: e.key, items: e.value))
            .toList();

        return movie.copyWith(episodes: episodeServers);
      }
    } catch (_) {}
    return null;
  }
}
