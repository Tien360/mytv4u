with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "if (_tmdbDetails != null) ...[" in line and "status" not in line:
        # Check if next line has status
        if i+1 < len(lines) and "status" in lines[i+1]:
            for j in range(i, i+60):
                print(f"{j+1}: {lines[j].encode('ascii', 'ignore').decode('ascii').rstrip()}")
            break
