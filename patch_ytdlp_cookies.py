import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update _fetchYtQualities
fetch_old = """        final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';
        
        final res = await Process.run(exePath, ['--no-playlist', '-J', url]);"""

fetch_new = """        final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';
        
        final appDataDir = await getApplicationSupportDirectory();
        final profileDir = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView');
        
        final res = await Process.run(exePath, [
          '--cookies-from-browser', 'edge=$profileDir',
          '--no-playlist', '-J', url
        ]);"""
content = content.replace(fetch_old, fetch_new.replace('edge=', 'edge:'))


# 2. Update player property for cookies
init_old = """      try {
        (player.platform as dynamic).setProperty('hwdec', 'auto-safe');
      } catch (_) {}"""

init_new = """      try {
        (player.platform as dynamic).setProperty('hwdec', 'auto-safe');
        final appDataDir = await getApplicationSupportDirectory();
        final profileDir = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView').replaceAll(r'\\', '/');
        (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=edge:$profileDir');
      } catch (_) {}"""
content = content.replace(init_old, init_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart")
