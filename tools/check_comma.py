import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r',\s*,', text)
for m in matches:
    print(f"Double comma found at {m.start()}")

matches2 = re.finditer(r',\s*\]', text)
for m in matches2:
    # trailing comma is allowed in Dart.
    pass

matches3 = re.finditer(r'\[\s*,', text)
for m in matches3:
    print(f"Comma after opening bracket found at {m.start()}")
