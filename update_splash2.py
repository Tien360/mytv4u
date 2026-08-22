import re

with open('lib/screens/splash_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("split('\\').last.split('/').last", r"split(r'\').last.split('/').last")
content = content.replace("replaceAll('\\', '/')", r"replaceAll(r'\', '/')")

with open('lib/screens/splash_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed splash_screen.dart")
