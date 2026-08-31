import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure dart:convert and webview_windows are imported
imports = "import 'dart:convert';\nimport 'package:webview_windows/webview_windows.dart';"
if "import 'package:webview_windows/webview_windows.dart';" not in content:
    content = content.replace("import 'package:shared_preferences/shared_preferences.dart';", "import 'package:shared_preferences/shared_preferences.dart';\n" + imports)

# Replace the yt-dlp playlist parsing logic with DOM Scraping if isYtLinked is true
search = """                              if (isYtLinked) {
                                final appDataDir = await getApplicationSupportDirectory();
                                final ebPath = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView');
                                args.insert(0, 'edge:$ebPath');
                                args.insert(0, '--cookies-from-browser');
                              }
                              
                              ProcessResult res = await Process.run(exePath, args);
                              if (res.exitCode != 0 && isYtLinked) {
                                // Fallback
                                res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
                              }
                              
                              if (res.exitCode == 0) {
                                final lines = res.stdout.toString().split('\n').where((l) => l.trim().isNotEmpty).toList();
                                if (lines.length > 1) {
                                  movieName = 'Playlist (${lines.length})';
                                  for (var line in lines) {
                                    try {
                                      final j = jsonDecode(line);
                                      if (j['id'] != null) {
                                        eps.add(Episode(
                                          name: j['title'] ?? 'Video',
                                          slug: j['id'],
                                          m3u8Url: 'https://www.youtube.com/watch?v=${j['id']}'
                                        ));
                                      }
                                    } catch (_) {}
                                  }
                                } else if (lines.length == 1) {
                                  try {
                                    final j = jsonDecode(lines.first);
                                    movieName = j['title'] ?? 'Video';
                                  } catch (_) {}
                                  eps.add(Episode(name: movieName, slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                                } else {
                                  eps.add(Episode(name: 'Stream', slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                                }
                              } else {
                                eps.add(Episode(name: 'Stream', slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                              }"""

new_logic = """                              bool usedScraper = false;
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
                              }
                              
                              if (!usedScraper) {
                                ProcessResult res = await Process.run(exePath, args);
                                if (res.exitCode == 0) {
                                  final lines = res.stdout.toString().split('\\n').where((l) => l.trim().isNotEmpty).toList();
                                  if (lines.length > 1) {
                                    movieName = 'Playlist (${lines.length})';
                                    for (var line in lines) {
                                      try {
                                        final j = jsonDecode(line);
                                        if (j['id'] != null) {
                                          eps.add(Episode(
                                            name: j['title'] ?? 'Video',
                                            slug: j['id'],
                                            m3u8Url: 'https://www.youtube.com/watch?v=${j['id']}'
                                          ));
                                        }
                                      } catch (_) {}
                                    }
                                  } else if (lines.length == 1) {
                                    try {
                                      final j = jsonDecode(lines.first);
                                      movieName = j['title'] ?? 'Video';
                                    } catch (_) {}
                                    eps.add(Episode(name: movieName, slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                                  } else {
                                    eps.add(Episode(name: 'Stream', slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                                  }
                                } else {
                                  eps.add(Episode(name: 'Stream', slug: 'stream_${DateTime.now().millisecondsSinceEpoch}', m3u8Url: url));
                                }
                              }"""

content = content.replace(search, new_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched library_screen.dart with DOM Scraper")
