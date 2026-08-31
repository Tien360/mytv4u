import re

for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/movie_detail_screen_test.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update _pauseTrailer
    pattern_pause = r'  Future<void> _pauseTrailer\(\) async \{.*?\n  \}'
    new_pause = """  Future<void> _pauseTrailer() async {
    _userPausedTrailer = true;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.loadUrl('about:blank');
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

    # 2. Update _playTrailer
    pattern_play = r'  void _playTrailer\(\) \{.*?\}\s*\}'
    new_play = """  void _playTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      await _webviewController.loadUrl('http://127.0.0.1:$_trailerPort/trailer.html?autoplay=1');
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

    # 3. Update _resumeTrailer
    pattern_resume = r'  void _resumeTrailer\(\) \{.*?\}\s*\}'
    new_resume = """  void _resumeTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      await _webviewController.loadUrl('http://127.0.0.1:$_trailerPort/trailer.html?autoplay=1');
      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
          _isTrailerPaused = false;
        });
      }
    }
  }"""
    c = re.sub(pattern_resume, new_resume, c, flags=re.DOTALL, count=1)

    # 4. Update the HTTP server logic to handle ?autoplay=1
    pattern_server = r"      if \(request\.uri\.path == '/trailer\.html'\) \{\s*final html =\s*'''"
    new_server = """      if (request.uri.path == '/trailer.html') {
        final forceAutoplay = request.uri.queryParameters['autoplay'] == '1';
        final shouldAutoplay = forceAutoplay || _autoPlayTrailerSetting;
        final html =
            '''"""
    c = re.sub(pattern_server, new_server, c, count=1)

    # 5. Update autoplay inside HTML
    c = c.replace("'autoplay': ${_autoPlayTrailerSetting ? 1 : 0},", "'autoplay': ${shouldAutoplay ? 1 : 0},")
    c = c.replace("${_autoPlayTrailerSetting ? 'event.target.playVideo();' : ''}", "${shouldAutoplay ? 'event.target.playVideo();' : ''}")

    # 6. Fix _startInlineTrailer loadUrl to pass autoplay=1 if _autoPlayTrailerSetting is true (or just let the server handle it based on shouldAutoplay)
    # The URL in _startInlineTrailer is `final url = 'http://127.0.0.1:$_trailerPort/trailer.html';` which is fine, shouldAutoplay will fallback to _autoPlayTrailerSetting.

    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Updated pause/play logic!")
