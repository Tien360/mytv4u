with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[930:1030]):
    print(f"{931+i}: {line.rstrip()}")
