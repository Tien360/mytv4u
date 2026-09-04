with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old = "this.progress = 0.0,\n    this.progressColor = Colors.redAccent,"
new = "this.progress = 0.5,\n    this.progressColor = Colors.redAccent,"

c = c.replace(old, new)
c = c.replace("if (widget.progress > 0)", "if (true)")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Forced progress UI to show")
