with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {\n  final ScrollController _mainScrollController = ScrollController();", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {")
c = c.replace("_mainScrollController.dispose();\n    super.dispose();", "super.dispose();")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed controller")
