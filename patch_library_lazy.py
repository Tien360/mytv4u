import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the scraping logic with the instant play bypass
search = """                              bool usedScraper = false;
                              if (isYtLinked && (url.contains('list=') || url.contains('playlist?'))) {
                                // Use Headless WebView DOM Scraping
                                try {
                                  final appDataDir = await getApplicationSupportDirectory();
                                  final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
                                  try { await WebviewController.initializeEnvironment(userDataPath: profileDir); } catch(e){}
                                  final _c = WebviewController();
                                  await _c.initialize();
                                  await _c.loadUrl(url);
                                  
                                  for (int i=0; i<8; i++) {
                                    await Future.delayed(const Duration(seconds: 1));
                                    if (!_c.value.isInitialized) break;
                                    
                                    final js = '''
                                      (function() {
                                        var items = document.querySelectorAll('ytd-playlist-panel-video-renderer, ytd-playlist-video-renderer');
                                        if (items.length === 0) return null;
                                        var arr = [];
                                        items.forEach(function(el) {
                                          var a = el.querySelector('a#wc-endpoint, a.yt-simple-endpoint');
                                          if (a && a.href) {
                                            var titleEl = el.querySelector('#video-title');
                                            var title = titleEl ? titleEl.innerText.trim() : "";
                                            try {
                                              var urlObj = new URL(a.href);
                                              var id = urlObj.searchParams.get('v');
                                              if (id && title) arr.push({id: id, title: title});
                                            } catch(e){}
                                          }
                                        });
                                        return arr.length > 0 ? JSON.stringify(arr) : null;
                                      })();
                                    ''';
                                    
                                    final result = await _c.executeScript(js) as String?;
                                    if (result != null && result != "null") {
                                      final List<dynamic> parsed = jsonDecode(result);
                                      if (parsed.isNotEmpty) {
                                        movieName = 'My Mix (${parsed.length})';
                                        for (var item in parsed) {
                                          eps.add(Episode(
                                            name: item['title'],
                                            slug: item['id'],
                                            m3u8Url: 'https://www.youtube.com/watch?v=' + item['id']
                                          ));
                                        }
                                        usedScraper = true;
                                        break;
                                      }
                                    }
                                  }
                                  await _c.dispose();
                                } catch(e) {
                                  print('Scraper error: $e');
                                }
                              }"""

new_logic = """                              bool usedScraper = false;
                              if (isYtLinked && url.contains('v=') && (url.contains('list=') || url.contains('playlist?'))) {
                                // INSTANT PLAY + LAZY LOAD PLAYLIST (Background Scraping)
                                try {
                                  final uri = Uri.parse(url);
                                  final v = uri.queryParameters['v'];
                                  if (v != null) {
                                    eps.add(Episode(
                                      name: 'Đang tải danh sách Mix/Playlist...',
                                      slug: v,
                                      m3u8Url: 'https://www.youtube.com/watch?v=$v'
                                    ));
                                    
                                    if (mounted) {
                                      Navigator.pop(context); // close dialog
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (_) => PlayerScreen(
                                            episodes: eps,
                                            currentEpisodeIndex: 0,
                                            movieName: 'YouTube Mix / Playlist',
                                            lazyPlaylistUrl: url,
                                          ),
                                        ),
                                      );
                                    }
                                    return; // completely skip yt-dlp loading!
                                  }
                                } catch(e) {}
                              }"""

content = content.replace(search, new_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched library_screen.dart")
