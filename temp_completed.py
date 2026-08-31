content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
idx = content.find("player.stream.completed.listen")
open('temp.txt', 'w', encoding='utf-8').write(content[idx:idx+1000])
