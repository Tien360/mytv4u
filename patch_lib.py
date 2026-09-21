import re

with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add import if not present
if "yt_player_screen.dart" not in content:
    content = content.replace("import 'player_screen.dart';", "import 'player_screen.dart';\nimport 'yt_player_screen.dart';")

replacement = """
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
                                  movieName: 'Lu?ng M?ng',
                                  isLive: _isLive,
                                ),
                              ),
                            );
                          }
                        }
"""

content = re.sub(r"if \(url\.isNotEmpty\) \{.*?Navigator\.pop\(context\);.*?Navigator\.push\(.*?builder: \(\_\) => PlayerScreen\(.*?isLive: _isLive,.*?\},.*?\},", replacement.strip(), content, flags=re.DOTALL)

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
