path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Tab Chung' in line:
        for j in range(i, i+150):
            if j < len(lines):
                print(f"{j}: {lines[j].rstrip()}")
        break
