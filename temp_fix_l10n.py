import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import '../l10n/l10n.dart';", "import '../utils/l10n.dart';")

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed l10n import")
