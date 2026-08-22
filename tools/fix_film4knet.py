
import re

with open('lib/api/film4knet_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''
        // Parse episodes
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
        
        // If single movie, sources are directly in movieData
        if (movieData['hlsUrl'] != null && isValidUrl(movieData['hlsUrl'])) {
          String serverName = 'Film4K Archive';
          servers[serverName] = [
            Episode(
              name: 'Full',
              slug: 'full',
              m3u8Url: buildFullUrl(movieData['hlsUrl']),
              embedUrl: '',
            )
          ];
        } else if (movieData['sources'] != null) {
          for (var src in movieData['sources']) {
            String url = src['url'] ?? '';
            if (isValidUrl(url)) {
              String serverName = src['label'] ?? 'Film4K Archive';
              if (!servers.containsKey(serverName)) servers[serverName] = [];
              servers[serverName]!.add(Episode(
                name: 'Full',
                slug: 'full',
                m3u8Url: buildFullUrl(url),
                embedUrl: '',
              ));
            }
          }
        }
        
        // If series, sources are in episodes array
        final epsList = data['episodes'] as List? ?? [];
        for (var ep in epsList) {
          String epName = ep['title'] ?? 'Tập ';
          final sources = ep['sources'] as List? ?? [];
          for (var src in sources) {
            String url = src['url'] ?? '';
            if (isValidUrl(url)) {
              String serverName = src['label'] ?? 'Film4K Archive';
              if (!servers.containsKey(serverName)) servers[serverName] = [];
              servers[serverName]!.add(Episode(
                name: epName,
                slug: '-',
                m3u8Url: buildFullUrl(url),
                embedUrl: '',
              ));
            }
          }
        }
'''

# Use regex to replace the entire episodes parsing block
text = re.sub(r'// Parse episodes.*?(?=final episodeServers)', replacement.strip() + '\n\n        ', text, flags=re.DOTALL)

with open('lib/api/film4knet_api.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

