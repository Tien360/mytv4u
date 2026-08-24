with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
pattern = r"_buildSectionTitle\(\s*Icons\.auto_awesome,[\s\S]*?_buildSettingToggle\([\s\S]*?enable_easter_eggs[\s\S]*?\}\,\s*\),"
text = re.sub(pattern, "", text)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned up old block 2!")
