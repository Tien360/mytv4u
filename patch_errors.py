import re

# 1. Fix library_screen.dart
path_lib = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path_lib, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("setState(() {\n                            _isLoadingUrl = true;\n                          });", "")
content = content.replace("setState(() {\n                              _isLoadingUrl = false;\n                            });", "")
with open(path_lib, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Fix settings_screen.dart
path_set = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path_set, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to add _defaultRepeat, _defaultSleepTimer, and _ytCookieSource
# Search for _backgroundPlayback = false;
var_search = "bool _backgroundPlayback = false;"
var_inject = "bool _backgroundPlayback = false;\n  bool _defaultRepeat = false;\n  int _defaultSleepTimer = 0;\n  String _ytCookieSource = 'none';\n"
if "String _ytCookieSource = 'none';" not in content:
    content = content.replace(var_search, var_inject)

# Also fix the load logic
load_search = "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;\n    _ytCookieSource = _prefs!.getString('yt_cookie_source') ?? 'none';"
if load_search not in content:
    old_load = "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;"
    new_load = "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;\n    _ytCookieSource = _prefs!.getString('yt_cookie_source') ?? 'none';\n    _defaultRepeat = _prefs!.getBool('default_repeat') ?? false;\n    _defaultSleepTimer = _prefs!.getInt('default_sleep_timer') ?? 0;"
    content = content.replace(old_load, new_load)

with open(path_set, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed errors")
