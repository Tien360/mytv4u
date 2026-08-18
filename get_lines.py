with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[740:830]):
    print(f"{741+i}: {line.rstrip()}")
