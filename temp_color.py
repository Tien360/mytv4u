content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("SizedBox(key: _colorKey)")
print(content[idx-100:idx+800])
