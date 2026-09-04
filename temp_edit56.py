import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'return Padding\(\s*child:\s*GestureDetector\(',
    r'return GestureDetector(',
    c
)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed Padding error in PlayerScreen")
