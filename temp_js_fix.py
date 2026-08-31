import re

for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/movie_detail_screen_test.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()

    # Add initialization guard
    if "bool _isInitializingWebview = false;" not in c:
        c = c.replace("bool _isWebviewInitialized = false;", "bool _isWebviewInitialized = false;\n  bool _isInitializingWebview = false;")

    # Fix _startInlineTrailer
    pattern_start = r'  void _startInlineTrailer\(\) async \{.*?\n  \}'
    new_start = """  void _startInlineTrailer() async {
    if (_movie == null || _movie!.trailerUrl == null || _movie!.trailerUrl!.isEmpty) return;
    if (_isInitializingWebview) return;
    
    _isInitializingWebview = true;
    final ytKey = _movie!.trailerUrl!.split('v=').last;
    if (!_isWebviewInitialized) {
      try {
        await _webviewController.initialize();
        _isWebviewInitialized = true;
        await _initWebview(ytKey);
        
        final url = 'http://127.0.0.1:$_trailerPort/trailer.html';
        await _webviewController.loadUrl(url);

        if (mounted) {
          setState(() {
            _showInlineTrailer = true;
          });
        }
      } catch (e) {}
    }
    _isInitializingWebview = false;
  }"""
    c = re.sub(pattern_start, new_start, c, flags=re.DOTALL)

    # Fix _pauseTrailer
    pattern_pause = r'  Future<void> _pauseTrailer\(\) async \{.*?\n  \}'
    new_pause = """  Future<void> _pauseTrailer() async {
    _userPausedTrailer = true;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "window.dartShouldPause = true; if(typeof player !== 'undefined' && player && player.pauseVideo) { player.pauseVideo(); }"
        );
      } catch (e) {}
    }
    if (mounted) {
      setState(() {
        _showInlineTrailer = false;
        _isTrailerPaused = true;
        _isTrailerExpanded = false;
      });
    }
  }"""
    c = re.sub(pattern_pause, new_pause, c, flags=re.DOTALL)

    # Fix _playTrailer
    pattern_play = r'  void _playTrailer\(\) async \{.*?\}\s*\}'
    new_play = """  void _playTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "if(typeof player !== 'undefined' && player && player.playVideo) { player.playVideo(); }"
        );
      } catch (e) {}
      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
          _isTrailerPaused = false;
          _trailerEnded = false;
          _isTrailerExpanded = false;
        });
      }
    } else {
      _startInlineTrailer();
    }
  }"""
    c = re.sub(pattern_play, new_play, c, flags=re.DOTALL, count=1)

    # Fix _resumeTrailer
    pattern_resume = r'  void _resumeTrailer\(\) async \{.*?\}\s*\}'
    new_resume = """  void _resumeTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "if(typeof player !== 'undefined' && player && player.playVideo) { player.playVideo(); }"
        );
      } catch (e) {}
      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
          _isTrailerPaused = false;
        });
      }
    }
  }"""
    c = re.sub(pattern_resume, new_resume, c, flags=re.DOTALL, count=1)

    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Updated JS logic!")
