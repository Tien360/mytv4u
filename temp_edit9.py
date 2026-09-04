with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re
# Replace onTap: () { if (director['id'] ...
c = re.sub(
    r'onTap: \(\) \{\s*if \(director\[\'id\'\]',
    r'onTap: () async {\n                                                          if (director[\'id\']',
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed director onTap with regex")
