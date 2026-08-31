import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\minion_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Spray Effect
content = content.replace(".moveY(begin: 0, end: 350, duration: 600.ms, curve: Curves.easeInBack)", ".moveY(begin: -350, end: 0, duration: 600.ms, curve: Curves.easeInBack)")

# Fix Guitar Effect
content = content.replace(".moveX(begin: 0, end: 320, duration: 800.ms, curve: Curves.easeInCirc)", ".moveX(begin: -320, end: 0, duration: 800.ms, curve: Curves.easeInCirc)")

# Fix Confused Effect
content = content.replace(".moveX(begin: 0, end: -320, duration: 800.ms, curve: Curves.easeInBack)", ".moveX(begin: 320, end: 0, duration: 800.ms, curve: Curves.easeInBack)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed minion_easter_egg.dart animations")
