import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace cookieSource logic
old_logic = """      final prefs = await SharedPreferences.getInstance();
      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      List<String> args = ['-J', '--flat-playlist', url];
      if (cookieSource != 'none') {
        if (cookieSource == 'webview') {
          final appDataDir = await getApplicationSupportDirectory();
          final ebPath = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView');
          args.insert(0, 'edge:$ebPath');
          args.insert(0, '--cookies-from-browser');
        } else {
          args.insert(0, cookieSource);
          args.insert(0, '--cookies-from-browser');
        }
      }
      
      ProcessResult res = await Process.run(exePath, args);
      if (res.exitCode != 0 && cookieSource != 'none') {"""

new_logic = """      final prefs = await SharedPreferences.getInstance();
      final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
      List<String> args = ['-J', '--flat-playlist', url];
      if (isYtLinked) {
        final appDataDir = await getApplicationSupportDirectory();
        final ebPath = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView');
        args.insert(0, 'edge:$ebPath');
        args.insert(0, '--cookies-from-browser');
      }
      
      ProcessResult res = await Process.run(exePath, args);
      if (res.exitCode != 0 && isYtLinked) {"""

content = content.replace(old_logic, new_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart")
