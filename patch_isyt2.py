path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("_prefs = await SharedPreferences.getInstance();", "_prefs = await SharedPreferences.getInstance();\n    setState(() { _isYtLinked = _prefs!.getBool('is_yt_linked') ?? false; });")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added setState loading logic")
