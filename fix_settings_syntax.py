import re

with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the corrupted declaration block
content = content.replace(
"""  bool _ambientBg = true;
                  globalEnableAmbient.value = true;
                  _hwAccel = true;
  bool _ambientBg = true;""",
"  bool _hwAccel = true;\n  bool _ambientBg = true;"
)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
