import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove duplicate int _systemRamMB = 4096;
    # We will replace all occurrences with a unique placeholder, then put it back once.
    content = content.replace('int _systemRamMB = 4096;', '')
    content = content.replace('bool _isPlayerInitialized = false;', 'bool _isPlayerInitialized = false;\n  int _systemRamMB = 4096;')
    content = content.replace('bool _isPlayerInit = false;', 'bool _isPlayerInit = false;\n  int _systemRamMB = 4096;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('lib/screens/player_screen.dart')
fix_file('lib/screens/tv_player_screen.dart')
