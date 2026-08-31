import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\spider_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_show = """  static void show(BuildContext context) {"""
new_show = """  import 'package:shared_preferences/shared_preferences.dart';
  
  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
"""

if "SharedPreferences" not in content:
    content = content.replace("import 'package:media_kit/media_kit.dart';", "import 'package:media_kit/media_kit.dart';\nimport 'package:shared_preferences/shared_preferences.dart';")
    content = content.replace("static void show(BuildContext context) {", """static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;""")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated spider_easter_egg.dart with SharedPreferences check")
