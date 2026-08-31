import re
content = open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8').read()
content = re.sub(r'SwitchListTile\(\s*activeColor: Colors\.blueAccent,\s*title: Text\(\s*L10n\.t\(\'auto_next_ep\'\).*?setTabState\(\(\) \{\}\);\s*\},\s*\),', '', content, flags=re.DOTALL)
open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8').write(content)
