import re
with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("extends State<MovieDetailScreen>", "extends State<MovieDetailScreenTest>")
c = c.replace("=> MovieDetailScreen(", "=> MovieDetailScreenTest(")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed type errors")
