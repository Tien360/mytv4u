import re

def revert_play_tv_channel(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Re-add import
    content = content.replace("import 'tv_player_screen.dart';", "import 'tv_player_screen.dart';\nimport 'tv_webview_screen.dart';")

    # Replace _playTvChannel logic
    pattern = r"void _playTvChannel\(TvChannel channel\) async \{.*?(?=final allTvEpisodes =)"
    
    replacement = '''void _playTvChannel(TvChannel channel) {
    if (channel.streamUrl.isEmpty && channel.webUrl.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) =>
              TvWebViewScreen(title: channel.name, webUrl: channel.webUrl),
        ),
      );
      return;
    }

    '''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_play_tv_channel('lib/screens/tv_screen.dart')
print("Reverted tv_screen.dart")
