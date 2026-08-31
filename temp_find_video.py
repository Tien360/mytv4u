import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find("SizedBox(key: _videoKey)")
idx2 = content.find("SizedBox(key: _audioKey)")

if idx1 != -1 and idx2 != -1:
    print(content[idx1:idx1+800])
