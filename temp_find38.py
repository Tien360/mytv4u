import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("L10n.t('default_speed')")
if idx != -1:
    print(repr(content[idx:idx+800]))
else:
    print("Could not find default_speed block!")
