import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('// Ignore id3 parsing errors\n    }', '// Ignore id3 parsing errors\n    }\n    _updateDominantColor();')
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
