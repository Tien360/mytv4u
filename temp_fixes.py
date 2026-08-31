with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Fix constructor
c = c.replace("const MovieDetailScreen({", "const MovieDetailScreenTest({")

# Fix controller
c = c.replace("controller: _mainScrollController,\n                  child: CustomScrollView(", "child: CustomScrollView(\n                    controller: _mainScrollController,")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed")
