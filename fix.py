import io

with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            if (movieSeasonMatch.isNotEmpty) {
              inferredSeason = int.tryParse(movieSeasonMatch.last.group(1)!);
            } else {
                    inferredSeason = 1;
                  }
                }'''

replacement = '''            if (movieSeasonMatch.isNotEmpty) {
              inferredSeason = int.tryParse(movieSeasonMatch.last.group(1)!);
            } else {
              inferredSeason = 1;
            }
          }
                }'''

if target in text:
    text = text.replace(target, replacement)
    with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced!")
else:
    print("Not found")
