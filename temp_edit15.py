with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# Remove dart:math
c = c.replace("import 'dart:math' as math;\n", "")
c = c.replace("import 'dart:math';\n", "")

c = re.sub(
    r"final double fraction = math\.max\(0\.05, posMs / durMs\)\.clamp\(0\.0, 1\.0\);",
    r"""double fraction = 0.05;
              if (durMs > 0) {
                fraction = (posMs / durMs).clamp(0.0, 1.0);
              }
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;""",
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed math issue")
