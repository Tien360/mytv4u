
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
import re
lines = content.split('\n')
for i, line in enumerate(lines[:150]):
    if 'PlayerScreen' in line or 'videoUrl' in line or 'media_kit' in line or 'Media' in line:
        print(f'{i+1}: {line.strip()}')

