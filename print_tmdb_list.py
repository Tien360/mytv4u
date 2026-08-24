with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Widget _buildTmdbHorizontalList(" in line:
        for j in range(max(0, i-2), min(len(lines), i+80)):
            print(f"{j+1}: {lines[j].encode('ascii', 'ignore').decode('ascii').rstrip()}")
        break
