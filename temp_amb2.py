import sys
with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("AmbientBackground(imageUrl: currentThumb)", "AmbientBackground()")

if "globalAmbientImageUrl.value = " not in c:
    c = c.replace("return Scaffold(", "globalAmbientImageUrl.value = currentThumb;\n    return Scaffold(")
    c = c.replace("import '../widgets/ambient_background.dart';", "import '../widgets/ambient_background.dart';\nimport '../globals.dart';")

with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print("fixed AmbientBackground")
