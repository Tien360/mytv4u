with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "if (_tmdbDetails != null) ...[" in line:
        print(f"Found at line {i+1}")
