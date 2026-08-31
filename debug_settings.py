path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(1350, 1390):
    if j < len(lines):
        print(f"{j+1}: {lines[j].rstrip()}")
