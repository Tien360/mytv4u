import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert YouTube after Search
pattern_search = r"(_buildNavItem\(\s*Icons\.search_outlined,\s*Icons\.search,\s*L10n\.t\('nav_search'\),\s*2,\s*\),\s*const SizedBox\(height: 8\),)"
replacement_youtube = r"""\1
                          _buildNavItem(
                            Icons.smart_display_outlined,
                            Icons.smart_display,
                            'YouTube',
                            3,
                          ),
                          const SizedBox(height: 8),"""
content = re.sub(pattern_search, replacement_youtube, content)

# Shift indices for subsequent items
# TV is 3 -> 4
content = re.sub(r"L10n\.t\('nav_tv'\),\s*3,", r"L10n.t('nav_tv'),\n                            4,", content)
# Sport is 4 -> 5
content = re.sub(r"L10n\.t\('nav_sport'\) \?\? '[^']*',\s*4,", r"L10n.t('nav_sport') ?? 'Thể Thao',\n                            5,", content)
# Library is 5 -> 6
content = re.sub(r"L10n\.t\('nav_library'\) \?\? '[^']*',\s*5,", r"L10n.t('nav_library') ?? 'Thư viện',\n                            6,", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated sidebar")
