path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'void _showSettingsDialog() async {' in line:
        open_brackets = 0
        found_bracket = False
        for j in range(i, len(lines)):
            if '{' in lines[j]:
                open_brackets += lines[j].count('{')
                found_bracket = True
            if '}' in lines[j]:
                open_brackets -= lines[j].count('}')
            if found_bracket and open_brackets == 0:
                print(f"End of method at line {j+1}: {lines[j].strip()}")
                break
        break
