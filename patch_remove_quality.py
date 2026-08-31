import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r"if \(_movie!\.quality\.isNotEmpty\)\s+_buildBadge\(\s+_movie!\.quality,\s+Colors\.greenAccent,\s+\),")

if pattern.search(content):
    content = pattern.sub("", content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed quality badge successfully.")
else:
    print("Failed to find quality badge.")
