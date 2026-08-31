content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("_buildNextEpisodeOverlay()")
open('temp.txt', 'w', encoding='utf-8').write(content[idx:idx+2500])
