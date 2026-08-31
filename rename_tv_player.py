import codecs

with codecs.open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("class PlayerScreen extends StatefulWidget", "class TvPlayerScreen extends StatefulWidget")
code = code.replace("const PlayerScreen({", "const TvPlayerScreen({")
code = code.replace("State<PlayerScreen> createState() => _PlayerScreenState();", "State<TvPlayerScreen> createState() => _TvPlayerScreenState();")
code = code.replace("class _PlayerScreenState extends State<PlayerScreen>", "class _TvPlayerScreenState extends State<TvPlayerScreen>")

with codecs.open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Renamed classes in tv_player_screen.dart")
