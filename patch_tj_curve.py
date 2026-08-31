import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\tom_jerry_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Curves.easeOutBounce", "Curves.bounceOut")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed curve")
