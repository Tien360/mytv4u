
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Media(' in line or 'player.open(' in line:
        print(f'{i+1}: {line.strip()}')

