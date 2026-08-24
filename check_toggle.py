with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re

# find where _buildSettingToggle is used.
matches = re.findall(r"_buildSettingToggle", text)
print("Count of _buildSettingToggle: ", len(matches))
