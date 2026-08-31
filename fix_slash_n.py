import os
content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('\\\\n                // Next Episode Overlay', '\\n                // Next Episode Overlay')
open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
