import re

def revert_ytdl(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ytdl block we inserted and revert it back to simple ytdl-format
    start_str = "if (_isYoutubeLink) {"
    end_str = "await player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)
    
    if start_idx != -1 and end_idx != -1:
        new_block = '''if (_isYoutubeLink) {
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
        await player.open(Media(_currentUrl, httpHeaders: headers), play: false);'''
        
        content = content[:start_idx] + new_block + content[end_idx:]
        print("Reverted successfully!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_ytdl('lib/screens/player_screen.dart')
