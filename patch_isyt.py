path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Load _isYtLinked when screen loads
old_load = """      _easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;"""
new_load = """      _easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;
      _isYtLinked = _prefs!.getBool('is_yt_linked') ?? false;"""

content = content.replace(old_load, new_load)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added _isYtLinked loading logic")
