with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("widthFactor: widget.progress.clamp(0.0, 1.0),", "widthFactor: (widget.progress > 0 ? widget.progress : 0.5).clamp(0.0, 1.0),")
c = c.replace("child: Container(color: widget.progressColor),", "child: Container(color: Colors.red),")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Forced progress UI to show correctly")
