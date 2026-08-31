content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("L10n.t('resume_watching')")
open('temp.txt', 'w', encoding='utf-8').write(content[idx+600:idx+1500])
