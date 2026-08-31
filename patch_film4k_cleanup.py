import re

with open('lib/api/film4knet_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's cleanly remove all getDetail methods and insert exactly one.
parts = text.split("static Future<Movie?> getDetail(String slug) async {")
prefix = parts[0]

new_getDetail = """static Future<Movie?> getDetail(String slug) async {
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
"""

with open('lib/api/film4knet_api.dart', 'w', encoding='utf-8') as f:
    f.write(prefix + new_getDetail)

print("Cleaned up duplicated getDetail")
