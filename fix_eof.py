import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('      ),\n      ),\n    );\n  }\n}\n', '      ),\n      ),\n      ),\n    );\n  }\n}\n')
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
