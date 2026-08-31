content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("SizedBox(key: _audioKey)")
open('temp.txt', 'w', encoding='utf-8').write(content[idx+2000:idx+3500])
