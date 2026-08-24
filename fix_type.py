with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace Function(dynamic) with void Function(dynamic)
text = text.replace("final Function(dynamic) onSearchAndPlay;", "final void Function(dynamic) onSearchAndPlay;")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed type error in TmdbHorizontalList")
