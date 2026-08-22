
import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to remove Tooltip with Icons.hd and its Tab
text = re.sub(r'\s*Tooltip\(\s*message:.*?child:\s*Tab\(\s*icon:\s*Icon\(Icons\.hd\).*?\),\s*\),', '', text, flags=re.DOTALL)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

