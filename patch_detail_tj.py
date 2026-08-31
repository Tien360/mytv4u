import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "tom_jerry_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/fast_furious_easter_egg.dart';", "import '../widgets/fast_furious_easter_egg.dart';\nimport '../widgets/tom_jerry_easter_egg.dart';")

trigger_logic = """if (queryLower.contains('fast and furious') || queryLower.contains('fast & furious') || queryLower.contains('qu\u00e1 nhanh qu\u00e1 nguy hi\u1ec3m') || queryLower.contains('toretto') || queryLower.contains('dominic')) {
        FastFuriousEasterEgg.show(context);
      }
      if (queryLower.contains('tom and jerry') || queryLower.contains('tom & jerry') || queryLower.contains('tom v\u00e0 jerry') || queryLower.contains('tom va jerry')) {
        TomJerryEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower\.contains\('fast and furious'\)[\s\S]*?FastFuriousEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart for TJ")
