import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if "kungfu_panda_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/minion_easter_egg.dart';", "import '../widgets/minion_easter_egg.dart';\nimport '../widgets/kungfu_panda_easter_egg.dart';")

# Add trigger logic
trigger_logic = """if (queryLower.contains('minion') || queryLower.contains('k\u1ebb tr\u1ed9m m\u1eb7t tr\u0103ng') || queryLower.contains('ke trom mat trang') || queryLower.contains('despicable me') || queryLower.contains('gru')) {
        MinionEasterEgg.show(context);
      }
      if (queryLower.contains('kung fu panda') || queryLower.contains('kungfu panda') || queryLower.contains('g\u1ea5u tr\u00fac') || queryLower.contains('gau truc') || queryLower.contains('th\u1ea7n long \u0111\u1ea1i hi\u1ec7p') || queryLower.contains('po')) {
        KungfuPandaEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower\.contains\('minion'\)[\s\S]*?MinionEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart")
