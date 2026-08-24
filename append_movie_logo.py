with open("AnimatedMovieLogoWidget.dart", "rb") as f:
    widget_code = f.read().replace(b'\xef\xbb\xbf', b'').decode('utf-8')

with open("lib/screens/movie_detail_screen.dart", "a", encoding="utf-8") as f:
    f.write("\n" + widget_code + "\n")
print("Appended AnimatedMovieLogoWidget!")
