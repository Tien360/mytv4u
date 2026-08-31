import re

path = r"T:\Project\Phim\mytv4u_flutter\tools\release.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_gh = """final ghPath = 'gh';
  if (File(ghPath).existsSync()) {"""
new_gh = """final ghPath = 'gh';
  if (true) {"""

content = content.replace(old_gh, new_gh)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched gh check")
