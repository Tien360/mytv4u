import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'    \);\s*void _showOpenUrlDialog', '    );\n  }\n\n  void _showOpenUrlDialog', content)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed braces properly")
