import sys

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Rename classes
c = c.replace("class MovieDetailScreen extends", "class MovieDetailScreenTest extends")
c = c.replace("class _MovieDetailScreenState extends State<MovieDetailScreen>", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest>")
c = c.replace("State<MovieDetailScreen> createState() => _MovieDetailScreenState();", "State<MovieDetailScreenTest> createState() => _MovieDetailScreenTestState();")
c = c.replace("=> MovieDetailScreen(", "=> MovieDetailScreenTest(")
c = c.replace("const MovieDetailScreen({", "const MovieDetailScreenTest({")

# 2. Add Test indicator to title
c = c.replace("title: _movie!.name,", "title: '${_movie!.name} (\U0001f9ea Bản Test)',")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Reverted to base")
