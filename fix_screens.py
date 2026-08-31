import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(SearchScreen\(key: _searchKey\),)"
replacement = r"\1\n      const YoutubeScreen(key: PageStorageKey('YoutubeScreen')),"

content = re.sub(pattern, replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed _screens array")
