import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = "import '../widgets/image_gallery_viewer.dart';"
new_import = "import '../widgets/image_gallery_viewer.dart';\nimport '../widgets/spider_easter_egg.dart';"

content = content.replace(import_statement, new_import)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched imports in movie_detail_screen.dart")
