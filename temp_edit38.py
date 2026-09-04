import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_str = "final targetPrefix = 'continue_${_movie!.name}_'.toLowerCase();"
new_str = "final targetPrefix = 'continue_${_movie!.name.trim()}_'.toLowerCase();"
c = c.replace(old_str, new_str)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Added trim() to targetPrefix")
