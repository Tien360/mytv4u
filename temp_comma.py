import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

pattern = r"(_buildRichText\('\$\{L10n\.t\('status'\) \?\? 'Trạng thái'\}: ', _translateStatus\(_tmdbDetails!\['status'\]\.toString\(\)\)\))\s*if \(isSeries\)"
replacement = r"\1,\n                                                  if (isSeries)"
if re.search(pattern, c):
    c = re.sub(pattern, replacement, c)
    print("Fixed comma")
else:
    print("Pattern not found")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
