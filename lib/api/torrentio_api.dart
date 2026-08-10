import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/movie.dart';
import 'stremio_server.dart';

/// Torrentio API service - fetches torrent streams from the Torrentio Stremio addon
/// and converts them into Episode objects playable via the local Stremio server.
class TorrentioApi {
  static const String _torrentioBase = 'https://torrentio.strem.fun';
  static const String _tmdbApiKey = 'e9e9d8da18ae29fc430845952232787c';

  /// Search TMDB for a movie/series and return its IMDB ID.
  /// Returns null if not found.
  static Future<String?> getImdbId(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    try {
      // Clean up titles (remove 'Season X', 'Phần X', etc.) for better TMDB search
      String cleanTitle(String t) {
        final regex = RegExp(r'(?:\s*-\s*)?(?:season|phần|part)\s*\d+', caseSensitive: false);
        return t.replaceAll(regex, '').trim();
      }
      
      final cTitle = cleanTitle(title);
      final cOriginal = cleanTitle(originalTitle);

      final query = Uri.encodeComponent(
          cOriginal.isNotEmpty ? cOriginal : cTitle);
      final searchUrl =
          'https://api.themoviedb.org/3/search/${isTvSeries ? 'tv' : 'movie'}?query=$query&api_key=$_tmdbApiKey&language=en-US';

      final res = await http.get(Uri.parse(searchUrl)).timeout(const Duration(seconds: 5));
      if (res.statusCode != 200) return null;

      final data = json.decode(res.body);
      final results = data['results'] as List?;
      if (results == null || results.isEmpty) return null;

      // Find best match by year
      var match = results[0];
      if (year.isNotEmpty) {
        final yMatch = results.firstWhere(
          (r) => (r['release_date'] ?? r['first_air_date'] ?? '')
              .toString()
              .startsWith(year),
          orElse: () => null,
        );
        if (yMatch != null) match = yMatch;
      }

      final tmdbId = match['id'];
      final type = isTvSeries ? 'tv' : 'movie';

      // Get external IDs (IMDB ID) from TMDB
      final extUrl =
          'https://api.themoviedb.org/3/$type/$tmdbId/external_ids?api_key=$_tmdbApiKey';
      final extRes = await http.get(Uri.parse(extUrl)).timeout(const Duration(seconds: 5));
      if (extRes.statusCode == 200) {
        final extData = json.decode(extRes.body);
        final imdbId = extData['imdb_id'];
        if (imdbId != null && imdbId.toString().startsWith('tt')) {
          return imdbId.toString();
        }
      }
    } catch (e) {
      print('TorrentioApi.getImdbId error: $e');
    }
    return null;
  }

  /// Get TMDB ID from IMDB ID using TMDB Find API
  static Future<String?> getTmdbIdFromImdb(String imdbId) async {
    try {
      final url = 'https://api.themoviedb.org/3/find/$imdbId?external_source=imdb_id&api_key=$_tmdbApiKey';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        if (data['movie_results'] != null && data['movie_results'].isNotEmpty) {
          return data['movie_results'][0]['id'].toString();
        } else if (data['tv_results'] != null && data['tv_results'].isNotEmpty) {
          return data['tv_results'][0]['id'].toString();
        }
      }
    } catch (e) {
      print('TorrentioApi.getTmdbIdFromImdb error: $e');
    }
    return null;
  }

  /// Fetch available torrent streams for a movie from Torrentio and PirateBay.
  /// Returns a list of EpisodeServer objects containing playable streams.
  static Future<List<EpisodeServer>> fetchStreams(
    String imdbId, {
    int? season,
    int? episode,
  }) async {
    try {
      // Build the Torrentio API URL
      String type;
      String id;
      if (season != null && episode != null) {
        type = 'series';
        id = '$imdbId:$season:$episode';
      } else {
        type = 'movie';
        id = imdbId;
      }

      final torrentioUrl = '$_torrentioBase/stream/$type/$id.json';
      final tpbUrl = 'https://thepiratebay-plus.strem.fun/stream/$type/$id.json';

      print('TorrentApi: Fetching streams from $torrentioUrl and $tpbUrl');

      // Fetch from both concurrently
      final responses = await Future.wait([
        http.get(Uri.parse(torrentioUrl)).timeout(const Duration(seconds: 25)).catchError((_) => http.Response('', 500)),
        http.get(Uri.parse(tpbUrl)).timeout(const Duration(seconds: 15)).catchError((_) => http.Response('', 500)),
      ]);

      final List<dynamic> allStreamsData = [];

      for (var res in responses) {
        if (res.statusCode == 200 && res.body.isNotEmpty) {
          try {
            final data = json.decode(res.body);
            final streams = data['streams'] as List? ?? [];
            allStreamsData.addAll(streams);
          } catch (_) {}
        }
      }

      if (allStreamsData.isEmpty) {
        print('TorrentApi: No streams found for $id');
        return [];
      }

      print('TorrentApi: Found ${allStreamsData.length} streams in total');

      // Convert torrent streams to Episode objects
      final List<Episode> allEpisodes = [];

      // Sort streams by seeders (descending) by extracting the number after 👤
      allStreamsData.sort((a, b) {
        final titleA = (a['title'] ?? '').toString();
        final titleB = (b['title'] ?? '').toString();
        
        final seedA = int.tryParse(RegExp(r'👤\s*(\d+)').firstMatch(titleA)?.group(1) ?? '0') ?? 0;
        final seedB = int.tryParse(RegExp(r'👤\s*(\d+)').firstMatch(titleB)?.group(1) ?? '0') ?? 0;
        
        return seedB.compareTo(seedA); // descending
      });

      // Limit to top 50 streams
      final topStreams = allStreamsData.take(50).toList();

      for (int i = 0; i < topStreams.length; i++) {
        final stream = topStreams[i] as Map<String, dynamic>;
        final infoHash = stream['infoHash'] as String?;
        if (infoHash == null || infoHash.isEmpty) continue;

        final fileIdx = stream['fileIdx'] as int? ?? 0;
        final title = stream['title']?.toString() ?? '';
        final name = stream['name']?.toString() ?? 'Torrent';

        // Parse quality, size, and source from the title
        final displayName = _parseStreamDisplayName(title, name, i + 1);

        // Build the local streaming URL via Stremio server
        final streamUrl = StremioServer.buildStreamUrl(infoHash, fileIdx);

        allEpisodes.add(Episode(
          name: displayName,
          slug: 'torrent-$i',
          m3u8Url: streamUrl,
          embedUrl: '',
        ));
      }

      if (allEpisodes.isEmpty) return [];

      return [
        EpisodeServer(
          serverName: '🌐 Torrent (P2P)',
          items: allEpisodes,
        ),
      ];
    } catch (e) {
      print('TorrentioApi.fetchStreams error: $e');
      return [];
    }
  }

  /// Parse stream title into a readable display name.
  /// Example input: "The.Movie.2024.1080p.BluRay.x264\n👤 15 💾 2.5 GB 📦 YTS"
  /// Example output: "1080p · 2.5 GB · YTS · 15 seeds"
  static String _parseStreamDisplayName(String title, String name, int index) {
    // Extract quality
    String quality = '';
    if (title.contains('2160p') || title.contains('4K') || title.contains('4k')) {
      quality = '4K';
    } else if (title.contains('1080p')) {
      quality = '1080p';
    } else if (title.contains('720p')) {
      quality = '720p';
    } else if (title.contains('480p')) {
      quality = '480p';
    } else {
      quality = 'SD';
    }

    // Extract codec info
    String codec = '';
    if (title.contains('HEVC') || title.contains('x265') || title.contains('H.265')) {
      codec = 'HEVC';
    } else if (title.contains('x264') || title.contains('H.264')) {
      codec = 'H264';
    }

    // Extract HDR info
    String hdr = '';
    if (title.contains('DV') || title.contains('Dolby Vision')) {
      hdr = 'DV';
    } else if (title.contains('HDR10+')) {
      hdr = 'HDR10+';
    } else if (title.contains('HDR')) {
      hdr = 'HDR';
    }

    // Extract size (e.g., "💾 2.5 GB" or "💾 850 MB")
    String size = '';
    final sizeMatch = RegExp(r'(\d+\.?\d*)\s*(GB|MB|TB)', caseSensitive: false).firstMatch(title);
    if (sizeMatch != null) {
      size = '${sizeMatch.group(1)} ${sizeMatch.group(2)}';
    }

    // Extract seeders (e.g., "👤 15")
    String seeds = '';
    final seedMatch = RegExp(r'👤\s*(\d+)').firstMatch(title);
    if (seedMatch != null) {
      seeds = '${seedMatch.group(1)} seeds';
    }

    // Extract source (e.g., "📦 YTS" or "📦 1337x" or from the name field)
    String source = '';
    final sourceMatch = RegExp(r'📦\s*(\S+)').firstMatch(title);
    if (sourceMatch != null) {
      source = sourceMatch.group(1) ?? '';
    } else {
      if (name.contains('TPB')) {
        source = 'PirateBay';
      } else {
        source = 'Torrentio';
      }
    }

    // Build display name
    final parts = <String>[quality];
    if (codec.isNotEmpty) parts.add(codec);
    if (hdr.isNotEmpty) parts.add(hdr);
    if (size.isNotEmpty) parts.add(size);
    if (source.isNotEmpty) parts.add(source);
    if (seeds.isNotEmpty) parts.add(seeds);

    return parts.join(' · ');
  }
}
