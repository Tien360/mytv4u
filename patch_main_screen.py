import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = "import '../widgets/ambient_background.dart';"
new_import = "import '../widgets/ambient_background.dart';\nimport '../widgets/spider_easter_egg.dart';"

if "spider_easter_egg.dart" not in content:
    content = content.replace(import_statement, new_import)

trigger_logic = """onSubmitted: (value) {
                              if (_selectedIndex == 3) {"""

new_trigger_logic = """onSubmitted: (value) {
                              // Easter Egg check
                              final queryLower = value.toLowerCase();
                              if (queryLower.contains('spider man') || queryLower.contains('spiderman') || queryLower.contains('người nhện') || queryLower.contains('nguoi nhen') || queryLower.contains('peter parker')) {
                                SpiderEasterEgg.show(context);
                              }
                              
                              if (_selectedIndex == 3) {"""

content = content.replace(trigger_logic, new_trigger_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched main_screen.dart")
