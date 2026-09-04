with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

new_func = """  Future<void> _saveDummyProgressForWebview() async {
    final prefs = await SharedPreferences.getInstance();
    final ep = _episodes[_currentIndex];
    final key = 'continue_${widget.movieName}_${ep.name}';
    final durKey = 'continue_duration_${widget.movieName}_${ep.name}';
    
    final currentPos = prefs.getInt(key) ?? 0;
    if (currentPos == 0) {
      await prefs.setInt(key, 1); // 1 ms to trigger the 5% fallback
      await prefs.setInt(durKey, 0);
    }
  }

  Future<void> _saveLocalProgress() async {"""

c = c.replace("  Future<void> _saveLocalProgress() async {", new_func)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Injected _saveDummyProgressForWebview correctly")
