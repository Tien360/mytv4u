def fix_ytdl_format(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    replacement = '''if (_isYoutubeLink) {
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
           player.platform?.setProperty('ytdl-format', 'bestvideo[height<=?'+heightTarget+']+bestaudio/best');
        } catch(e) {}
      }
      player.open(Media(_currentUrl, httpHeaders: headers), play: false);'''
    
    if "heightTarget =" not in content:
        content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_ytdl_format('lib/screens/player_screen.dart')
print("Fixed ytdl-format injection")
