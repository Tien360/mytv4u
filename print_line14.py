with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"1614: {lines[1613].strip()}")
print(f"1692: {lines[1691].strip()}")
for i in range(1680, 1700):
    print(f"{i+1}: {lines[i].rstrip()}")
