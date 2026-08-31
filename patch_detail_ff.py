import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "fast_furious_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/kungfu_panda_easter_egg.dart';", "import '../widgets/kungfu_panda_easter_egg.dart';\nimport '../widgets/fast_furious_easter_egg.dart';")

trigger_logic = """if (queryLower.contains('kung fu panda') || queryLower.contains('kungfu panda') || queryLower.contains('g\u1ea5u tr\u00fac') || queryLower.contains('gau truc') || queryLower.contains('th\u1ea7n long \u0111\u1ea1i hi\u1ec7p') || queryLower.contains('po')) {
        KungfuPandaEasterEgg.show(context);
      }
      if (queryLower.contains('fast and furious') || queryLower.contains('fast & furious') || queryLower.contains('qu\u00e1 nhanh qu\u00e1 nguy hi\u1ec3m') || queryLower.contains('toretto') || queryLower.contains('dominic')) {
        FastFuriousEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower\.contains\('kung fu panda'\)[\s\S]*?KungfuPandaEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart for FF")
