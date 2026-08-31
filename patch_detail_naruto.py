import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "naruto_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/tom_jerry_easter_egg.dart';", "import '../widgets/tom_jerry_easter_egg.dart';\nimport '../widgets/naruto_easter_egg.dart';")

trigger_logic = """if (queryLower.contains('tom and jerry') || queryLower.contains('tom & jerry') || queryLower.contains('tom v\u00e0 jerry') || queryLower.contains('tom va jerry')) {
        TomJerryEasterEgg.show(context);
      }
      if (queryLower.contains('naruto') || queryLower.contains('sasuke') || queryLower.contains('kakashi') || queryLower.contains('hokage') || queryLower.contains('akatsuki') || queryLower.contains('c\u1eedu v\u0129') || queryLower.contains('boruto')) {
        NarutoEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower\.contains\('tom and jerry'\)[\s\S]*?TomJerryEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart for Naruto")
