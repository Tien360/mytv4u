import sys
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("if (_movie!.isSeries) ...[", "if (isSeries) ...[")
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed isSeries")
