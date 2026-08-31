path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '// 2. Controls Layer' in line:
        for j in range(i-5, i+15):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
