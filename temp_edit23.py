with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Replace classes
c = c.replace("MovieDetailScreenTest", "MovieDetailScreen")
c = c.replace("_MovieDetailScreenTestState", "_MovieDetailScreenState")

# Remove " (🧪 Bản Test)"
c = c.replace(" (🧪 Bản Test)", "")
c = c.replace("import 'movie_detail_screen_test.dart';", "")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Overwritten movie_detail_screen.dart")
