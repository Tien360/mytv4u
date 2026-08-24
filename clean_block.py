with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find the block from _buildSectionTitle(Icons.auto_awesome to the end of _buildSettingToggle
pattern = r"const SizedBox\(height: 16\);\s*_buildSectionTitle\(\s*Icons\.auto_awesome,[\s\S]*?enable_easter_eggs[\s\S]*?\}\,\s*\),"
text = re.sub(pattern, "", text)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned up old block!")
