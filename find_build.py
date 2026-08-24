with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Widget build(BuildContext context)" in line:
        print(f"Build method at line {i}")
        break
