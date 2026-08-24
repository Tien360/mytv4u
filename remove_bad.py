import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# I need to find `if (_directorsTmdb.isNotEmpty) ...[` and remove it until `],`
pattern_bad = r"\s*if \(_directorsTmdb\.isNotEmpty\) \.\.\.\[.*?\]\,\s*"
content = re.sub(pattern_bad, "\n", content, count=1, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Removed bad directors")
