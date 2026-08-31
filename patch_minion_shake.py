import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\minion_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the shake parameter
content = content.replace(".shake(hz: 8, amount: 5, duration: 1000.ms)", ".shake(hz: 8, duration: 1000.ms)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed minion_easter_egg.dart shake parameter")
