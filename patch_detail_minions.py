import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if "minion_easter_egg.dart" not in content:
    content = content.replace("import '../widgets/ironman_easter_egg.dart';", "import '../widgets/ironman_easter_egg.dart';\nimport '../widgets/minion_easter_egg.dart';")

# Add trigger logic
trigger_logic = """if (queryLower.contains('iron man') || queryLower.contains('ironman') || queryLower.contains('ng\u01b0\u1eddi s\u1eaft') || queryLower.contains('nguoi sat') || queryLower.contains('tony stark')) {
        IronmanEasterEgg.show(context);
      }
      if (queryLower.contains('minion') || queryLower.contains('k\u1ebb tr\u1ed9m m\u1eb7t tr\u0103ng') || queryLower.contains('ke trom mat trang') || queryLower.contains('despicable me') || queryLower.contains('gru')) {
        MinionEasterEgg.show(context);
      }"""
content = re.sub(
    r"if \(queryLower.contains\('iron man'\)[\s\S]*?IronmanEasterEgg\.show\(context\);\s*\}",
    trigger_logic,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen.dart")
