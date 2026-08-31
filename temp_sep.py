content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
a = content.find("SizedBox(key: _audioKey)")
b = content.find("SizedBox(key: _colorKey)")
print(content[b-100:b+50])
