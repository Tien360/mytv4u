import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("bestMeta['fallback_filename'] = ep['filename'];", "bestMeta!['fallback_filename'] = ep['filename'];")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed nullable error")
