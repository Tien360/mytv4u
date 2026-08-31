import re

content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

if "player.setRate(_playbackSpeed);" not in content:
    content = content.replace("await player.open(Media(mediaUrl, httpHeaders: _getHeaders()));", "await player.open(Media(mediaUrl, httpHeaders: _getHeaders()));\n      player.setRate(_playbackSpeed);")
    content = content.replace("await player.open(Media(finalUrl));", "await player.open(Media(finalUrl));\n      player.setRate(_playbackSpeed);")

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched setRate!")
