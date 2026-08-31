content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("SizedBox(key: _infoKey)")
info = content[idx:idx+2000]
print(info)
