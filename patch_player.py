import re

content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

content = content.replace("(_position.inSeconds >= _duration.inSeconds - 120)", "(_position.inSeconds >= _duration.inSeconds - 180)")
content = content.replace("(_duration.inSeconds - _position.inSeconds) <= 90", "(_duration.inSeconds - _position.inSeconds) <= 180")

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched player_screen!")
