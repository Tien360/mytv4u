import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and remove
pattern = r"(\s*// Repeat[\s\S]*?)(?=\s*// Next Episode Button \(Right side\))"
content = re.sub(pattern, "", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed buttons")
