with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "Navigator.push(",
    "await Navigator.push("
)
c = c.replace("await await", "await")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Added await to Navigator.push")
