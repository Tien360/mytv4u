import codecs

with codecs.open('lib/screens/tv_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("import 'player_screen.dart';", "import 'player_screen.dart';\nimport 'tv_player_screen.dart';")
code = code.replace("builder: (_) => PlayerScreen(", "builder: (_) => TvPlayerScreen(")

with codecs.open('lib/screens/tv_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated tv_screen.dart")
