import re

def fix_play(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'youtube_explode_dart.dart' not in content:
        content = "import 'package:youtube_explode_dart/youtube_explode_dart.dart';\n" + content

    old_code = r"if \(_isYoutubeLink\) \{\s*String heightTarget.*?await player\.open\(Media\(_currentUrl, httpHeaders: headers\), play: false\);"
    
    new_code = """String finalPlayUrl = _currentUrl;
        if (_isYoutubeLink) {
          try {
            var yt = YoutubeExplode();
            var manifest = await yt.videos.streamsClient.getManifest(_currentUrl);
            var muxed = manifest.muxed.sortByVideoQuality();
            if (muxed.isNotEmpty) {
              finalPlayUrl = muxed.first.url.toString();
            }
            yt.close();
          } catch (e) {
            debugPrint('youtube_explode_dart error: $e');
          }
        }
        await player.open(Media(finalPlayUrl, httpHeaders: headers), play: false);"""
        
    content = re.sub(old_code, new_code, content, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_play('lib/screens/player_screen.dart')
