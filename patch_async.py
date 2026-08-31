import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "import 'dart:async';" not in content:
    content = "import 'dart:async';\n" + content

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
