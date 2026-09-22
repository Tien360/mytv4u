with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

if "import 'yt_player_screen.dart';" not in content:
    content = content.replace("import 'player_screen.dart';", "import 'player_screen.dart';\nimport 'yt_player_screen.dart';")

import re
old_block = r"""
                        onPressed: \(\) \{
                          final url = _urlController\.text\.trim\(\);
                          if \(url\.isNotEmpty\) \{
                            Navigator\.pop\(context\);
                            Navigator\.push\(
                              context,
                              MaterialPageRoute\(
                                builder: \(\_\) => PlayerScreen\(
                                  episodes: \[
                                    Episode\(
                                      name: 'Stream',
                                      slug: 'stream',
                                      m3u8Url: url,
                                      embedUrl: '',
                                    \),
                                  \],
                                  currentEpisodeIndex: 0,
                                  movieName: 'Luồng Mạng',
                                  isLive: _isLive,
                                \),
                              \),
                            \);
                          \}
                        \},
"""

new_block = """
                        onPressed: () {
                          final url = _urlController.text.trim();
                          if (url.isNotEmpty) {
                            Navigator.pop(context);
                            
                            final isYt = url.contains('youtube.com') || url.contains('youtu.be');
                            if (isYt) {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => YtPlayerScreen(
                                      episodes: [
                                        Episode(
                                          name: 'YouTube',
                                          slug: 'yt',
                                          m3u8Url: url,
                                          embedUrl: '',
                                        ),
                                      ],
                                      currentEpisodeIndex: 0,
                                      movieName: 'YouTube Video',
                                      isLive: _isLive,
                                      lazyPlaylistUrl: url.contains('list=') ? url : null,
                                    ),
                                  ),
                                );
                            } else {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => PlayerScreen(
                                      episodes: [
                                        Episode(
                                          name: 'Stream',
                                          slug: 'stream',
                                          m3u8Url: url,
                                          embedUrl: '',
                                        ),
                                      ],
                                      currentEpisodeIndex: 0,
                                      movieName: 'Luồng Mạng',
                                      isLive: _isLive,
                                    ),
                                  ),
                                );
                            }
                          }
                        },
"""

content = re.sub(old_block.strip(), new_block.strip(), content, flags=re.DOTALL)

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
