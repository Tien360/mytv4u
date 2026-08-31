import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\minion_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(".png", ".gif")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated to .gif")
