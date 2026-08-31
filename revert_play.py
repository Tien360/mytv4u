import re

def revert_play(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove youtube_explode_dart import
    content = content.replace("import 'package:youtube_explode_dart/youtube_explode_dart.dart' as yt_explode;\n", "")

    # Revert _playCurrentUrl
    old_code = r"String finalPlayUrl = _currentUrl;.*?await player\.open\(Media\(finalPlayUrl, httpHeaders: headers\), play: false\);"
    
    new_code = """        if (_isYoutubeLink) {
            String heightTarget = '2160';
            if (_selectedYtQuality.contains('8K') || _selectedYtQuality.contains('4320')) heightTarget = '4320';
            else if (_selectedYtQuality.contains('4K') || _selectedYtQuality.contains('2160')) heightTarget = '2160';
            else if (_selectedYtQuality.contains('1440')) heightTarget = '1440';
            else if (_selectedYtQuality.contains('1080')) heightTarget = '1080';
            else if (_selectedYtQuality.contains('720')) heightTarget = '720';
            else if (_selectedYtQuality.contains('480')) heightTarget = '480';
            else if (_selectedYtQuality.contains('360')) heightTarget = '360';
            else if (_selectedYtQuality.contains('240')) heightTarget = '240';
            else if (_selectedYtQuality.contains('144')) heightTarget = '144';
            
            try {
               (player.platform as dynamic).setProperty('ytdl-format', 'bestvideo[height<=?'+heightTarget+']+bestaudio/best');
            } catch(e) {}
          }
          await player.open(Media(_currentUrl, httpHeaders: headers), play: false);"""
          
    content = re.sub(old_code, new_code, content, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Reverted _playCurrentUrl to use yt-dlp!")

revert_play('lib/screens/player_screen.dart')
