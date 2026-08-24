import re

with open("lib/screens/main_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "ambient_background.dart" not in content:
    content = content.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\nimport '../widgets/ambient_background.dart';")

# Replace Container(color: const Color(0xFF000000)) with AmbientBackground
content = content.replace("Container(color: const Color(0xFF000000)),", "const AmbientBackground(),")

with open("lib/screens/main_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
