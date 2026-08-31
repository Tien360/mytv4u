import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\update_dialog.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import if missing
if "glass_container.dart" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'glass_container.dart';")

old_ui = """child: Container(
          width: 450,
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.black.withValues(alpha: 0.6),
            borderRadius: BorderRadius.circular(24),
            border: Border.all(color: Colors.white10),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.5),
                blurRadius: 20,
                spreadRadius: 5,
              )
            ],
          ),"""

new_ui = """child: GlassContainer(
          width: 450,
          padding: const EdgeInsets.all(24),
          borderRadius: 24,"""

if old_ui in content:
    content = content.replace(old_ui, new_ui)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched update_dialog.dart")
else:
    print("Could not find old_ui in update_dialog.dart")
