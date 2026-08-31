content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
for i, line in enumerate(content.split('\n')):
    if 'SizedBox(key: _' in line:
        print(f"{i}: {line.strip()}")
