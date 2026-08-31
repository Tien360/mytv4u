content = open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8').read()

old_desc = "                    'Bạn đã xem đến ${_formatDuration(Duration(milliseconds: savedPos))}. Bạn muốn xem tiếp hay xem lại từ đầu?',"
new_desc = "                    L10n.t('resume_watching_desc')?.replaceAll('{time}', _formatDuration(Duration(milliseconds: savedPos))) ?? 'Bạn đã xem đến ${_formatDuration(Duration(milliseconds: savedPos))}. Bạn muốn xem tiếp hay xem lại từ đầu?',"

content = content.replace(old_desc, new_desc)
open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8').write(content)
