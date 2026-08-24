with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "L10n.t('directors') ?? " in line:
        print(f"Directors found at line {i+1}")
