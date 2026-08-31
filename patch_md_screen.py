import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = "import '../widgets/ambient_background.dart';"
new_import = "import '../widgets/ambient_background.dart';\nimport '../widgets/spider_easter_egg.dart';"

if "spider_easter_egg.dart" not in content:
    content = content.replace(import_statement, new_import)

init_state_logic = """  void initState() {
    super.initState();
    _loadSettings();
    _fetchDetail();"""

new_init_state_logic = """  void initState() {
    super.initState();
    _loadSettings();
    _fetchDetail();
    
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final queryLower = (widget.initialMovie?.name ?? '').toLowerCase() + ' ' + (widget.initialMovie?.originalName ?? '').toLowerCase();
      if (queryLower.contains('spider man') || queryLower.contains('spiderman') || queryLower.contains('người nhện') || queryLower.contains('nguoi nhen') || queryLower.contains('peter parker')) {
        SpiderEasterEgg.show(context);
      }
    });"""

content = content.replace(init_state_logic, new_init_state_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched movie_detail_screen.dart")
