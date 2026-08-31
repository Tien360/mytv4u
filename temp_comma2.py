import sys
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

target = "_translateStatus(_tmdbDetails!['status'].toString())),\n                                                  if (isSeries)"
replacement = "_translateStatus(_tmdbDetails!['status'].toString())),\n                                                  if (isSeries)"
if target in c:
    c = c.replace(target, replacement) # wait, I need to add a comma!
    
target = "_translateStatus(_tmdbDetails!['status'].toString())),\n                                                  if (isSeries)"
replacement = "_translateStatus(_tmdbDetails!['status'].toString())),\n,\n                                                  if (isSeries)"
# Let's just do:
import re
c = re.sub(r"(_translateStatus\(_tmdbDetails!\[\'status\'\]\.toString\(\)\)\))\s*if \(isSeries\)", r"\1,\n                                                  if (isSeries)", c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed comma 2")
