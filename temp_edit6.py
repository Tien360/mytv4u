with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()
import re
c = re.sub(
    r'(Navigator\.push\(\s*context,\s*MaterialPageRoute\(\s*builder: \(_\) => PlayerScreen\(.*?\),\s*\),\s*\);)',
    r'\1\n                  _loadEpisodeProgressAndColor();',
    c,
    flags=re.DOTALL
)
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated Navigator.push to reload progress")
