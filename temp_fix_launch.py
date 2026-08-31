import sys

with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target = """  void _launchGame() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PlayerScreen(
          movieName: _gameInfo?.title ?? widget.gameTitle,
          episodes: [
            Episode(
              name: _gameInfo?.title ?? widget.gameTitle,
              slug: 'game',
              m3u8Url: '',
              embedUrl: widget.gameUrl,
            )
          ],
          currentEpisodeIndex: 0,
          isLive: true,
        ),
      ),
    );
  }"""
new_target = """  void _launchGame() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GamePlayerScreen(
          gameUrl: widget.gameUrl,
          gameThumb: widget.initialThumb,
        ),
      ),
    );
  }"""

if target in c:
    c = c.replace(target, new_target)
    print("Replaced _launchGame")
else:
    print("Could not find target")

with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
