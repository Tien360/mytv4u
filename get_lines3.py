with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1355:1375]):
    print(f"{1356+i}: {line.rstrip()}")
