path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import '../widgets/audio_player_effects.dart';\n"
content = content.replace("import '../widgets/glass_container.dart';", import_line + "import '../widgets/glass_container.dart';")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Import added")
