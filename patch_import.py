with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "import 'package:flutter/material.dart';" in line:
        lines.insert(i+1, "import 'package:mytv4u_flutter/widgets/advanced_controls_panel.dart';\n")
        break

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(lines)
