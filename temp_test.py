content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("L10n.t('audio_player_title')")
open('temp.txt', 'w', encoding='utf-8').write(content[idx+500:idx+1500])
