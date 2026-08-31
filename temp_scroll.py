import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Add _mainScrollController
if "_mainScrollController" not in c:
    c = c.replace("class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {\n", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {\n  final ScrollController _mainScrollController = ScrollController();\n")
    
    # Dispose it
    c = c.replace("super.dispose();", "_mainScrollController.dispose();\n    super.dispose();")

# Replace _scrollController with _mainScrollController in the AnimatedBuilder
c = c.replace("animation: _scrollController,", "animation: _mainScrollController,")
c = c.replace("_scrollController.hasClients", "_mainScrollController.hasClients")
c = c.replace("_scrollController.offset", "_mainScrollController.offset")

# Add controller to CustomScrollView
c = c.replace("child: CustomScrollView(\n                    slivers:", "child: CustomScrollView(\n                    controller: _mainScrollController,\n                    slivers:")

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Added main scroll controller")
