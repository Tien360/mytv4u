import re

# Fix player_screen.dart
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('package:mytv4u/widgets/advanced_controls_panel.dart', 'package:mytv4u_flutter/widgets/advanced_controls_panel.dart')
with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix advanced_controls_panel.dart
with open('lib/widgets/advanced_controls_panel.dart', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('package:mytv4u/widgets/glass_container.dart', 'package:mytv4u_flutter/widgets/glass_container.dart')
with open('lib/widgets/advanced_controls_panel.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed!')
