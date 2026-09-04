with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
"""                                                        onTap: () {
                                                          if (director['id'] != null && director['id']!.isNotEmpty) {""",
"""                                                        onTap: () async {
                                                          if (director['id'] != null && director['id']!.isNotEmpty) {"""
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed director onTap to async")
