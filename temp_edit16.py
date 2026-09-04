with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("if (durMs > 0 && posMs > 0) {", "if (posMs > 0) {")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed durMs check")
