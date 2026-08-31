import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the second occurrence and remove it
    parts = content.split('int _systemRamMB = 4096;', 1)
    if len(parts) > 1:
        parts[1] = parts[1].replace('int _systemRamMB = 4096;', '')
        content = parts[0] + 'int _systemRamMB = 4096;' + parts[1]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('lib/screens/player_screen.dart')
fix_file('lib/screens/tv_player_screen.dart')
