import sys

with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target_controls = """          // Window Controls
          const Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: CustomTitleBar(),
          ),"""

if target_controls in c:
    c = c.replace(target_controls, "")
    c = c.replace("        ],\n      ),\n    );", target_controls + "\n        ],\n      ),\n    );")
    with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Moved Window Controls to top of Stack")
else:
    print("Could not find Window Controls")

