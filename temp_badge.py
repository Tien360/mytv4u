with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("'${widget.title} (dY  Bn Test)',", "'${widget.title} (Bản Test)',")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
