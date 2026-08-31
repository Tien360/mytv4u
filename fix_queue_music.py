import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

pattern = re.compile(r'IconButton\(\s*icon:\s*const Icon\(Icons\.queue_music.*?(?=\s*IconButton|\s*\])', re.DOTALL)

new_button = '''IconButton(
  icon: const Icon(Icons.queue_music, color: Colors.white),
  tooltip: L10n.t('playlist') ?? 'Danh sách phát',
  onPressed: () => setState(() => _showPlaylist = !_showPlaylist),
),'''

content = re.sub(pattern, new_button + '\n', content, count=1)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
