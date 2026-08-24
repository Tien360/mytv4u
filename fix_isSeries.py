import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"final bool isSeries =\s*_movie!\.episodes\.isNotEmpty && _movie!\.episodes\.first\.items\.length > 1;"

new_logic = """final bool isSeries = _movie!.type == 'series' || _movie!.slug.contains('phim-bo') ||
          (_movie!.episodes.isNotEmpty && _movie!.episodes.first.items.length > 1 && 
           !_movie!.episodes.first.items.any((e) => e.name.toLowerCase().contains('1080') || e.name.toLowerCase().contains('720') || e.name.toLowerCase().contains('4k')));"""

if re.search(pattern, content):
    content = re.sub(pattern, new_logic, content)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed isSeries!")
else:
    print("Could not find isSeries pattern")
