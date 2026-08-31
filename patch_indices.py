import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix TV index
content = re.sub(
    r"L10n\.t\('nav_tv'\),\s*4,",
    r"L10n.t('nav_tv'),\n                          3,",
    content
)

# Fix Sport index
content = re.sub(
    r"L10n\.t\('nav_sport'\) \?\? 'Thể Thao',\s*5,",
    r"L10n.t('nav_sport') ?? 'Thể Thao',\n                          4,",
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated indices")
