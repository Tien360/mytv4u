import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "String _ytCookieSource" not in content:
    content = content.replace("bool _defaultRepeat = false;", "bool _defaultRepeat = false;\n  String _ytCookieSource = 'none';\n  String _ytCookieFilePath = '';")

# Add load logic
load_search = """_defaultSleepTimer = prefs.getInt('default_sleep_timer') ?? 0;"""
load_new = """_defaultSleepTimer = prefs.getInt('default_sleep_timer') ?? 0;
      _ytCookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      _ytCookieFilePath = prefs.getString('yt_cookie_file') ?? '';"""
if load_search in content:
    content = content.replace(load_search, load_new)

# Add save logic
save_search = """await prefs.setInt('default_sleep_timer', _defaultSleepTimer);"""
save_new = """await prefs.setInt('default_sleep_timer', _defaultSleepTimer);
    await prefs.setString('yt_cookie_source', _ytCookieSource);
    await prefs.setString('yt_cookie_file', _ytCookieFilePath);"""
if save_search in content:
    content = content.replace(save_search, save_new)

# Add reset logic
reset_search = """_defaultSleepTimer = 0;"""
reset_new = """_defaultSleepTimer = 0;
      _ytCookieSource = 'none';
      _ytCookieFilePath = '';"""
if reset_search in content:
    content = content.replace(reset_search, reset_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added state to settings")
