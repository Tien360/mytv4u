import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if "ironman_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/spider_easter_egg.dart';", "import '../widgets/spider_easter_egg.dart';\nimport '../widgets/ironman_easter_egg.dart';")

# Add trigger logic
trigger_logic = """if (queryLower.contains('spider man') || queryLower.contains('spiderman') || queryLower.contains('ng\u01b0\u1eddi nh\u1ec7n') || queryLower.contains('nguoi nhen') || queryLower.contains('peter parker')) {
        SpiderEasterEgg.show(context);
      }
      if (queryLower.contains('iron man') || queryLower.contains('ironman') || queryLower.contains('ng\u01b0\u1eddi s\u1eaft') || queryLower.contains('nguoi sat') || queryLower.contains('tony stark')) {
        IronmanEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower.contains\('spider man'\)[\s\S]*?SpiderEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart")
