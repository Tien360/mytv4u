import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '_showEpisodePanel = !_showEpisodePanel,',
    '_showEpisodePanel = !_showEpisodePanel;\n                                                if (_showEpisodePanel) _showAdvancedPanel = false;'
)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
