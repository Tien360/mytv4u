with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re
c = c.replace("final double fraction = (posMs / durMs).clamp(0.0, 1.0);", 
"""import 'dart:math' as math;
              final double fraction = math.max(0.05, posMs / durMs).clamp(0.0, 1.0);""")

c = c.replace("import 'dart:math' as math;", "") # remove if I accidentally inserted it multiple times
# let's just use 0.05 if it's less
c = c.replace("""final double fraction = (posMs / durMs).clamp(0.0, 1.0);""", 
"""double fraction = (posMs / durMs).clamp(0.0, 1.0);
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;""")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated fraction min logic")
