with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """
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
                          }
"""

new_block = """
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
                          }
"""

content = content.replace(old_block.strip(), new_block.strip())

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
