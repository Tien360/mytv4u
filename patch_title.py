import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "if (lines.length == 1 && json['playlist_title'] != null) {",
    "if (json['playlist_title'] != null && json['playlist_title'].toString().isNotEmpty) {"
)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
