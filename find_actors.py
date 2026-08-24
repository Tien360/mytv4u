with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "L10n.t('actors')" in line:
        print(f"Actors found at line {i+1}")
