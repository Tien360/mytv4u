import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fetch Qualities retry
fetch_search = """final res = await Process.run(exePath, args);
      if (res.exitCode == 0) {"""
fetch_new = """ProcessResult res = await Process.run(exePath, args);
      if (res.exitCode != 0 && cookieSource != 'none') {
        res = await Process.run(exePath, ['-J', url]);
      }
      if (res.exitCode == 0) {"""
if "ProcessResult res = await Process.run" not in content:
    content = content.replace(fetch_search, fetch_new)

# 2. Remove ytdl-raw-options for cookies
init_search = """      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      if (cookieSource != 'none' && _isYoutube) {
        (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=$cookieSource');
      } else {
        (player.platform as dynamic).setProperty('ytdl-raw-options', '');
      }"""
init_new = """      (player.platform as dynamic).setProperty('ytdl-raw-options', '');"""
content = content.replace(init_search, init_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed player_screen.dart")
