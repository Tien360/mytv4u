with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Remove the infinite recursion
target = """  @override
  Widget build(BuildContext context) {
    if (useTestDetailUi.value) {
      return MovieDetailScreenTest(
        slug: widget.slug,
        heroTag: widget.heroTag,
        initialMovie: widget.initialMovie,
      );
    }"""
    
replacement = """  @override
  Widget build(BuildContext context) {"""

c = c.replace(target, replacement)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed infinite recursion")
