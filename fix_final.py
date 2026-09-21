import shutil

shutil.copy("lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart")

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("PlayerScreen", "YtPlayerScreen")

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
