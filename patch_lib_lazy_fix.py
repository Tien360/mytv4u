import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = """                              final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
                              List<String> args = ['--dump-json', '--flat-playlist', url];"""
                              
new_logic = """                              final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
                              List<String> args = ['--dump-json', '--flat-playlist', url];
                              
                              if (isYtLinked && url.contains('v=') && (url.contains('list=') || url.contains('playlist?'))) {
                                try {
                                  final uri = Uri.parse(url);
                                  final v = uri.queryParameters['v'];
                                  if (v != null) {
                                    eps.add(Episode(
                                      name: 'Đang tải danh sách Mix/Playlist...',
                                      slug: v,
                                      m3u8Url: 'https://www.youtube.com/watch?v=$v',
                                      embedUrl: 'https://i.ytimg.com/vi/$v/maxresdefault.jpg'
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
                                    return; // skip yt-dlp
                                  }
                                } catch(e) {}
                              }"""

if "lazyPlaylistUrl" not in content:
    content = content.replace(search, new_logic)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched library_screen.dart")
else:
    print("Already patched")
