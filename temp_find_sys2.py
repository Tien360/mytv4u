import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find("SizedBox(key: _systemKey)")
idx2 = content.find("const SizedBox(height: 48)", idx1)

if idx1 != -1 and idx2 != -1:
    print(content[idx1:idx2])
