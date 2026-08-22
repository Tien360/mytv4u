import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix 1: Add missing Row for _sourcesKey
text = text.replace(
    "const SizedBox(height: 48),\n\n                          SizedBox(key: _sourcesKey),",
    "const SizedBox(height: 48),\n\n                          Row(\n                            mainAxisAlignment: MainAxisAlignment.spaceBetween,\n                            children: [\n                              SizedBox(key: _sourcesKey),"
)

# Fix 2: Remove the extra Row that was added before _colorKey
bad_row = '''                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
SizedBox(key: _colorKey),'''

good_color = '''SizedBox(key: _colorKey),'''

text = text.replace(bad_row, good_color)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print('Replaced')
