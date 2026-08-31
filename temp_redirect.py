import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import_str = "import 'movie_detail_screen_test.dart';\n"
c = c.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\n" + import_str)

redirect_code = """
  @override
  Widget build(BuildContext context) {
    if (useTestDetailUi.value) {
      return MovieDetailScreenTest(
        slug: widget.slug,
        heroTag: widget.heroTag,
        initialMovie: widget.initialMovie,
      );
    }
"""
c = c.replace("  @override\n  Widget build(BuildContext context) {", redirect_code, 1)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Redirect added")
