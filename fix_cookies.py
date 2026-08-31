import re

def fix_cookies(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ytdl-format section
    old_code = r"(player\.platform as dynamic)\.setProperty\('ytdl-format',\s*'bestvideo\[height<=\?'\+heightTarget\+'\]\+bestaudio/best'\);"
    
    new_code = '''(player.platform as dynamic).setProperty('ytdl-format', 'bestvideo[height<=?'+heightTarget+']+bestaudio/best');
           
           final prefs = await SharedPreferences.getInstance();
           final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
           if (isYtLinked) {
              final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
              final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
              (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=edge:' + defaultWebviewPath);
           }'''
           
    content = re.sub(old_code, new_code, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_cookies('lib/screens/player_screen.dart')
print("Patched cookies into media_kit")
