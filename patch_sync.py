import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

if "'enable_skip_intro'" not in content:
    content = content.replace("'enabled_sources',", "'enabled_sources',\n      'enable_skip_intro',\n      'skip_intro_duration',\n      'minimalist_ui',\n      'enable_ambient_bg',")

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched syncToFirebase!")
