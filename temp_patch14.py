import re
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

bad_str = """              ],
            ),
),
    );
  }

  Widget _buildSettingToggle({"""

good_str = """              ],
            ),
          ],
        ),
      );
  }

  Widget _buildSettingToggle({"""

if bad_str in content:
    content = content.replace(bad_str, good_str)
    print("Fixed login card closing brackets!")
else:
    print("Not found bad_str. Searching with regex...")
    # Just to be safe
    content = re.sub(
        r"              \],\n            \),\n\),\n    \);\n  }\n\n  Widget _buildSettingToggle",
        "              ],\n            ),\n          ],\n        ),\n      );\n  }\n\n  Widget _buildSettingToggle",
        content
    )
    print("Replaced with regex.")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
