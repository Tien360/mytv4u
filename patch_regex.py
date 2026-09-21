import io
import re
with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('r''(?:T[\\u1EA1a\\u1EAD\\u00E2]p|Ep)\s*0*(\d+)''', 'r''(?:T[\\u1EA1a\\u1EAD\\u00E2]p|Ep|E)\s*0*(\d+)''')
text = text.replace('r''(?:ph[\\u1EA7a]n|m[\\u00F9u]a|season|sesion|ss)\s*(\d+)'', caseSensitive: false).firstMatch(widget.movieName) ?? RegExp(r''S(\d+)E\d+'', caseSensitive: false).firstMatch(ep.name)', 'r''(?:ph[\\u1EA7a]n|m[\\u00F9u]a|season|sesion|ss|S)\s*0*(\d+)'', caseSensitive: false).firstMatch(ep.name) ?? RegExp(r''(?:ph[\\u1EA7a]n|m[\\u00F9u]a|season|sesion|ss)\s*(\d+)'', caseSensitive: false).firstMatch(widget.movieName)')
with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
