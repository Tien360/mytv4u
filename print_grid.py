with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "_buildEpisodesGrid()" in line:
        for j in range(i, i+50):
            print(f"{j+1}: {lines[j].encode('ascii', 'ignore').decode('ascii').rstrip()}")
        break
