import re

def fix_ytdl_path(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where we set ytdl-format
    # We want to replace everything around it cleanly.
    
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
             
             // 1. Force mpv to use our local yt-dlp.exe instead of failing if not in PATH
             File ytExe = File('${File(Platform.resolvedExecutable).parent.path}\\\\yt-dlp.exe');
             if (!ytExe.existsSync()) ytExe = File('build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe');
             if (ytExe.existsSync()) {
               (player.platform as dynamic).setProperty('script-opts', 'ytdl_hook-ytdl_path=' + ytExe.path.replaceAll('\\\\', '/'));
             }
             
             // 2. Pass Edge cookies if linked, so premium/music videos don't fail
             final prefs = await SharedPreferences.getInstance();
             if (prefs.getBool('is_yt_linked') == true) {
               final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
               final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
               (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=edge:' + defaultWebviewPath.replaceAll('\\\\', '/'));
             }
          } catch(e) {
             debugPrint('Failed to set ytdl properties: $e');
          }
        }
        await player.open(Media(_currentUrl, httpHeaders: headers), play: false);'''
        
        content = content[:start_idx] + new_block + content[end_idx:]
        print("Patched successfully!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_ytdl_path('lib/screens/player_screen.dart')
