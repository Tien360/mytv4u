import re

content = open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Remove child: _buildNextEpisodeOverlay(),
content = re.sub(r'child:\s*_buildNextEpisodeOverlay\(\),', 'child: const SizedBox(),', content)

# 2. Remove _buildNextEpisodeOverlay definition
content = re.sub(r'Widget _buildNextEpisodeOverlay\(\)\s*\{.*?\n  \}\n', '', content, flags=re.DOTALL)

open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8').write(content)
