with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("final void Function(dynamic) onSearchAndPlay;", "final void Function(Map<String, dynamic>) onSearchAndPlay;")
text = text.replace("widget.onSearchAndPlay(item),", "widget.onSearchAndPlay(item as Map<String, dynamic>),")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed type error with Map<String, dynamic>")
