import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'(\s*child:\s*Text\([\s\S]*?\),\s*\),\s*\),\s*)\);',
    r'\1',
    c
)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed syntax error in PlayerScreen")
