import re

path = r"T:\Project\Phim\mytv4u_flutter\pubspec.yaml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_assets = """    - assets/easter/"""
new_assets = """    - assets/easter/
    - assets/easter/spiderman/
    - assets/easter/sfx/"""

content = content.replace(old_assets, new_assets)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pubspec.yaml")
