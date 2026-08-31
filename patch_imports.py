import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "package:http/http.dart" not in content:
    content = "import 'package:http/http.dart' as http;\nimport 'dart:convert';\n" + content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Imported http and dart:convert")
