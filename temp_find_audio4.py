import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("SizedBox(key: _audioKey),")
idx2 = content.find("SizedBox(key: _sourcesKey),")
if idx != -1 and idx2 != -1:
    print(content[idx:idx2])
