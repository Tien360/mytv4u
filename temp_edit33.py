with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Replace all simple Navigator.push with await Navigator.push for PlayerScreen
# P2P Series block:
p2p_old = """                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: _currentServer!.items,
                          currentEpisodeIndex: index,
                          movieName: _movie!.name,
                          imdbId: _movie!.imdbId,
                          season: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(1)!) : null,
                          episode: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(2)!) : null,
                        ),
                      ),
                    );"""
p2p_new = """                    await Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: _currentServer!.items,
                          currentEpisodeIndex: index,
                          movieName: _movie!.name,
                          imdbId: _movie!.imdbId,
                          season: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(1)!) : null,
                          episode: seasonEpMatch != null ? int.tryParse(seasonEpMatch.group(2)!) : null,
                        ),
                      ),
                    );
                    _loadEpisodeProgressAndColor();"""
c = c.replace(p2p_old, p2p_new)

# Standard Embed Block:
std_old = """                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PlayerScreen(
                        episodes: items,
                        currentEpisodeIndex: index,
                        movieName: _movie!.name,
                        imdbId: _movie!.imdbId,
                      ),
                    ),
                  );"""
std_new = """                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PlayerScreen(
                        episodes: items,
                        currentEpisodeIndex: index,
                        movieName: _movie!.name,
                        imdbId: _movie!.imdbId,
                      ),
                    ),
                  );
                  _loadEpisodeProgressAndColor();"""
c = c.replace(std_old, std_new)

# Single / P2P stream block:
p2pstream_old = """                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: [_selectedP2pEpisode!],
                          currentEpisodeIndex: 0,
                          movieName: _movie!.name,
                          imdbId: _movie!.imdbId,
                          p2pStream: stream,
                        ),
                      ),
                    );"""
p2pstream_new = """                    await Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: [_selectedP2pEpisode!],
                          currentEpisodeIndex: 0,
                          movieName: _movie!.name,
                          imdbId: _movie!.imdbId,
                          p2pStream: stream,
                        ),
                      ),
                    );
                    _loadEpisodeProgressAndColor();"""
c = c.replace(p2pstream_old, p2pstream_new)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Injected await Navigator.push logic")
