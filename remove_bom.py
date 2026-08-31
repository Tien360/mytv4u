import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\tv_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the BOM if it exists anywhere
content = content.replace('\uFEFF', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed BOM from tv_screen.dart")
