with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Find the initialization of Webview where it loads the URL
old_wb = """        _isWebviewInitialized = true;
      }
      await _webController.loadUrl(_currentUrl);
      if (mounted) setState(() {});"""

new_wb = """        _isWebviewInitialized = true;
      }
      await _webController.loadUrl(_currentUrl);
      if (mounted) setState(() {});
      
      // Save a dummy progress (1 millisecond) so that it shows up as "watched" (5% bar) in MovieDetailScreen
      _saveDummyProgressForWebview();"""

c = c.replace(old_wb, new_wb)

# Inject the function
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

  void _saveLocalProgress() async {"""

c = c.replace("  void _saveLocalProgress() async {", new_func)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated player_screen.dart to save dummy progress for Webview")
