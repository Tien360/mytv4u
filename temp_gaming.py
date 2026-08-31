import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import 'game_webview_screen.dart';", "import 'player_screen.dart';\nimport '../models/movie.dart';")

old_launch = """  void _launchGame(String url, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GameWebViewScreen(title: title, webUrl: url),
      ),
    );
  }"""

new_launch = """  void _launchGame(String url, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PlayerScreen(
          movieName: title,
          episodes: [
            Episode(
              name: title,
              slug: 'game',
              m3u8Url: '',
              embedUrl: url,
            )
          ],
          currentEpisodeIndex: 0,
          isLive: true,
        ),
      ),
    );
  }"""

content = content.replace(old_launch, new_launch)
content = content.replace("https://play-lh.googleusercontent.com/D4s3L2P-uA6l2Qh6bTz7H2lXq7S1j-K3J_Y5_8T-M0D0sM-s1QZ0Y-7L0X0B_6F2W2U=w512-h512", "https://img.utdstc.com/icon/e19/39f/e1939faab6c7d1f1f1e53674c5b703f69c75ff345494a3c55b1d60e9f7014fdf:600")

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated gaming_screen.dart")
