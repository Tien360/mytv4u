import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"\](\s*)// Settings Gear Button", r"],\1// Settings Gear Button", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed syntax")
