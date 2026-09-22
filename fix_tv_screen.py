import re

with open("lib/screens/tv_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import 'tv_player_screen.dart';", "// import 'tv_player_screen.dart';")

with open("lib/screens/tv_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
