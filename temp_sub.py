content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("SizedBox(key: _subtitleKey)")
print(content[idx:idx+400])
