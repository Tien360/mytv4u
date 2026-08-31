with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

start = c.find("1. Background Media")
if start != -1:
    print(c[start:start+1000].encode("ascii", "ignore").decode("ascii"))
