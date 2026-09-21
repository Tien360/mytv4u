import re

with open("lib/api/premium_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the getter in premium_api.dart
if "static String? get medataDomain => _medataDomain;" not in content:
    # Just append it to the top of the class
    class_start = content.find("class PremiumApi {")
    if class_start != -1:
        insert_pos = content.find("\n", class_start) + 1
        content = content[:insert_pos] + "  static String? get medataDomain => _medataDomain;\n" + content[insert_pos:]

with open("lib/api/premium_api.dart", "w", encoding="utf-8") as f:
    f.write(content)


for file in ["lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()
    if "import 'package:mytv4u_flutter/api/premium_api.dart';" not in c:
        c = "import 'package:mytv4u_flutter/api/premium_api.dart';\n" + c
    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Fixed imports and getter")
