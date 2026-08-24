import re

with open("lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

if "ambient_background.dart" not in content:
    content = content.replace("import 'widgets/custom_title_bar.dart';", "import 'widgets/custom_title_bar.dart';\nimport 'widgets/ambient_background.dart';")

if "initAmbientSettings()" not in content:
    content = content.replace("await L10n.load();", "await L10n.load();\n  await initAmbientSettings();")

with open("lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
