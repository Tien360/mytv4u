with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

has_math = "import 'dart:math';" in text
if not has_math:
    text = text.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'dart:math';")
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)

with open("AnimatedLogoWidget.dart", "r", encoding="utf-8") as f:
    widget_code = f.read().replace("import 'dart:math';", "")

with open("lib/screens/movie_detail_screen.dart", "a", encoding="utf-8") as f:
    f.write("\n" + widget_code + "\n")
print("Appended AnimatedLogoWidget to movie_detail_screen.dart!")
