with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("player.stream.error.listen")
print(content[idx-200:idx+300])
