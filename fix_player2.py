import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("result != null && result.files.single.path != null", "result != null && result.isNotEmpty && result.single.path != null")
content = content.replace("result.files.single.path!", "result.single.path!")

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed player_screen.dart")
