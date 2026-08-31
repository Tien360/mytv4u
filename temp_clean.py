with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("class MovieDetailScreen extends", "class MovieDetailScreenTest extends")
c = c.replace("class _MovieDetailScreenState extends State<MovieDetailScreen>", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest>")
c = c.replace("State<MovieDetailScreen> createState() => _MovieDetailScreenState();", "State<MovieDetailScreenTest> createState() => _MovieDetailScreenTestState();")
c = c.replace("=> MovieDetailScreen(", "=> MovieDetailScreenTest(")
c = c.replace("const MovieDetailScreen({", "const MovieDetailScreenTest({")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Clean copy done")
