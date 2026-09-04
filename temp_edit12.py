with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
"""_dominantColor = paletteGenerator.dominantColor?.color ?? 
                             paletteGenerator.vibrantColor?.color ?? 
                             Colors.redAccent;""",
"""_dominantColor = paletteGenerator.vibrantColor?.color ?? 
                             paletteGenerator.dominantColor?.color ?? 
                             Colors.redAccent;"""
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated color priority")
