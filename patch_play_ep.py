import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "widget.episodes.add(Episode(\n                    name: item['title'],\n                    slug: item['id'],\n                    m3u8Url: 'https://www.youtube.com/watch?v=' + item['id']\n                  ));",
    "widget.episodes.add(Episode(\n                    name: item['title'],\n                    slug: item['id'],\n                    m3u8Url: 'https://www.youtube.com/watch?v=' + item['id'],\n                    embedUrl: 'https://i.ytimg.com/vi/' + item['id'] + '/maxresdefault.jpg'\n                  ));"
)

# Also fix the import 'package:path/path.dart' as p;
if "import 'package:path/path.dart' as p;" not in content:
    content = content.replace("import 'package:path_provider/path_provider.dart';", "import 'package:path_provider/path_provider.dart';\nimport 'package:path/path.dart' as p;")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed player_screen Episode and imports")
