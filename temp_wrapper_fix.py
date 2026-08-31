with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Fix initState
old_init = """  void initState() {
    super.initState();
    _loadSettings();
    _fetchDetail();"""

new_init = """  void initState() {
    super.initState();
    if (useTestDetailUi.value) return;
    
    _loadSettings();
    _fetchDetail();"""

c = c.replace(old_init, new_init)

# Fix dispose
old_dispose = """  void dispose() {
    _scrollController.dispose();
    _sweepController.dispose();"""

new_dispose = """  void dispose() {
    if (useTestDetailUi.value) {
      super.dispose();
      return;
    }
    _scrollController.dispose();
    _sweepController.dispose();"""

c = c.replace(old_dispose, new_dispose)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Added early return to original screen!")
