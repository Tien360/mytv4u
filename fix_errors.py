import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Define _toggleShuffle and _toggleRepeat
new_methods = '''  void _toggleShuffle() {
    setState(() {
      isShuffle = !isShuffle;
    });
  }

  void _toggleRepeat() {
    setState(() {
      repeatMode = (repeatMode + 1) % 3;
    });
  }

  void _next() {'''
content = content.replace('  void _next() {', new_methods)

# 2. Call _updateDominantColor
old_setState = '''      if (mounted) {
        setState(() {});
      }
    });'''
new_setState = '''      if (mounted) {
        setState(() {});
      }
      _updateDominantColor();
    });'''
content = content.replace(old_setState, new_setState)

# 3. Fix EOF closing parenthesis
if content.endswith('      ),\n    );\n  }\n}\n'):
    content = content.replace('      ),\n    );\n  }\n}\n', '      ),\n      ),\n    );\n  }\n}\n')

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
