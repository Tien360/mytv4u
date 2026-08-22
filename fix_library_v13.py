with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("path.replace('\\', '/')", r"path.replaceAll(r'\\', '/')")
if "import 'player_screen.dart';" not in content:
    content = "import 'player_screen.dart';\n" + content

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
