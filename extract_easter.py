with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
match = re.search(r"(\s*const SizedBox\(height: 16\);\s*_buildSectionTitle\([\s\S]*?easter_eggs_title[\s\S]*?_buildSettingToggle\([\s\S]*?\}\,\s*\)\,)", text)

if match:
    # Save the matched block
    with open("easter_block.txt", "w", encoding="utf-8") as f2:
        f2.write(match.group(1))
    print("Found Easter Block")
else:
    print("Not found")
