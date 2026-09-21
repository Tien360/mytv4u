import io

with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("} else {\n            final movieSeasonMatch = RegExp(r'(?:ph[ầa]n|m[ùu]a|season|sesion|ss)\s*0*(\d+)', caseSensitive: false).allMatches(widget.movieName);\n            if (movieSeasonMatch.isNotEmpty) {\n              inferredSeason = int.tryParse(movieSeasonMatch.last.group(1)!);\n            }\n          } else {", "} else {\n            final movieSeasonMatch = RegExp(r'(?:ph[ầa]n|m[ùu]a|season|sesion|ss)\s*0*(\d+)', caseSensitive: false).allMatches(widget.movieName);\n            if (movieSeasonMatch.isNotEmpty) {\n              inferredSeason = int.tryParse(movieSeasonMatch.last.group(1)!);\n            } else {")

with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
