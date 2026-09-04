with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("this.progress = 0.5,\n    this.progressColor = Colors.redAccent,", "this.progress = 0.0,\n    this.progressColor = Colors.redAccent,")
c = c.replace("if (true)", "if (widget.progress > 0)")
c = c.replace("widthFactor: (widget.progress > 0 ? widget.progress : 0.5).clamp(0.0, 1.0),", "widthFactor: widget.progress.clamp(0.0, 1.0),")
c = c.replace("child: Container(color: Colors.red),", "child: Container(color: widget.progressColor),")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Reverted hardcoded UI")
