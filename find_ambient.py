with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
match = re.search(r"SwitchListTile\([\s\S]*?ambient_bg[\s\S]*?\}\,\s*\)\,", text)
if match:
    print(match.group(0))
