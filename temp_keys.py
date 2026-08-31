import re
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
keys = re.findall(r'SizedBox\(key: _([a-zA-Z]+)Key\)', content)
print(keys)
