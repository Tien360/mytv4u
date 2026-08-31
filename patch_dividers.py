import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

# I want to make sure all Dividers between SwitchListTiles/ListTiles have height: 32
# specifically in the video block where I just added them.
# The ones I added were `const Divider(color: Colors.white12),`
content = content.replace("const Divider(color: Colors.white12),", "const Divider(color: Colors.white12, height: 32),")
content = content.replace("const Divider(color: Colors.white12),\n", "const Divider(color: Colors.white12, height: 32),\n")
# but maybe some already had height 32, so we don't want "height: 32, height: 32"
content = content.replace("height: 32, height: 32", "height: 32")

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched dividers!")
