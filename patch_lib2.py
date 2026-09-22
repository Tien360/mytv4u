import re

with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

replacement = """
                          final isYt = url.contains('youtube.com') || url.contains('youtu.be');
                          if (isYt) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => YtPlayerScreen(
                                  episodes: [
                                    Episode(
                                      name: 'YouTube Video',
                                      slug: 'yt',
                                      m3u8Url: url,
                                      embedUrl: '',
                                    ),
                                  ],
                                  currentEpisodeIndex: 0,
                                  movieName: 'YouTube',
                                  isLive: _isLive,
                                  lazyPlaylistUrl: url.contains('list=') ? url : null,
                                ),
                              ),
                            );
                          } else {
"""

content = re.sub(r"final isYt = url\.contains\('youtube\.com'\) \|\| url\.contains\('youtu\.be'\);\n\s*if \(isYt\) \{\n\s*Navigator\.push\(\n\s*context,\n\s*MaterialPageRoute\(\n\s*builder: \(\_\) => YtPlayerScreen\(\n\s*episodes: \[\n\s*Episode\(\n\s*name: 'YouTube',\n\s*slug: 'yt',\n\s*m3u8Url: url,\n\s*embedUrl: '',\n\s*\),\n\s*\],\n\s*currentEpisodeIndex: 0,\n\s*movieName: 'YouTube Video',\n\s*isLive: _isLive,\n\s*\),\n\s*\),\n\s*\);\n\s*\} else \{", replacement.strip(), content, flags=re.DOTALL)

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
