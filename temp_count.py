import re
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
print(content.count('SizedBox(key: _videoKey)'))
