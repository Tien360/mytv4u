import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "import 'youtube_screen.dart';" not in content:
    content = content.replace("import 'sport_screen.dart';", "import 'sport_screen.dart';\nimport 'youtube_screen.dart';")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed import")
