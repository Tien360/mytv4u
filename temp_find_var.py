with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "_isSubmittingComment" in line:
        print(f"Line {i+1}: {line.strip()}")
