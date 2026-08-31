import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Patch _fetchYtQualities
search_fetch = """final res = await Process.run(exePath, ['-J', url]);"""
new_fetch = """final prefs = await SharedPreferences.getInstance();
      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      List<String> args = ['-J', url];
      if (cookieSource != 'none') {
        args.insert(0, cookieSource);
        args.insert(0, '--cookies-from-browser');
      }
      final res = await Process.run(exePath, args);"""

if search_fetch in content:
    content = content.replace(search_fetch, new_fetch)

# 2. Patch _initEpisode with SharedPreferences
search_open = """player.open(Media(_currentUrl, httpHeaders: headers), play: false);"""
new_open = """
      final prefs = await SharedPreferences.getInstance();
      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      if (cookieSource != 'none' && _isYoutube) {
        (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=$cookieSource');
      } else {
        (player.platform as dynamic).setProperty('ytdl-raw-options', '');
      }
      
      player.open(Media(_currentUrl, httpHeaders: headers), play: false);"""

if search_open in content:
    content = content.replace(search_open, new_open)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart")
