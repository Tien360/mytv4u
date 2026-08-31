import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("hintText: _selectedIndex == 3", "hintText: _selectedIndex == 4")
content = content.replace(": _selectedIndex == 4\n                                  ? L10n.t('search_sports')", ": _selectedIndex == 5\n                                  ? L10n.t('search_sports')")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed hintText indices")
