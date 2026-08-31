import os
content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('(_duration.inSeconds - _position.inSeconds) <= 30', '(_duration.inSeconds - _position.inSeconds) <= 5')
open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
