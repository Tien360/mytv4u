import re

content = open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8').read()

# Replace the condition and Positioned with an empty string
content = re.sub(r'// Next Episode Overlay \(Near End\)\s*if \(!widget\.isLive &&.*?child:\s*const SizedBox\(\),\s*\),\s*\),', '', content, flags=re.DOTALL)

open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8').write(content)
