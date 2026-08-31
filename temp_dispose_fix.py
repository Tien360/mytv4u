with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_dispose = """  void dispose() {
    _movieSubscription?.cancel();"""

new_dispose = """  void dispose() {
    if (useTestDetailUi.value) {
      super.dispose();
      return;
    }
    _movieSubscription?.cancel();"""

c = c.replace(old_dispose, new_dispose)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed dispose!")
