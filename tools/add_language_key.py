import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

if 'final GlobalKey _languageKey = GlobalKey();' not in text:
    text = text.replace('final GlobalKey _subtitleKey = GlobalKey();', 'final GlobalKey _subtitleKey = GlobalKey();\n  final GlobalKey _languageKey = GlobalKey();')

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Language Key added")
