for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/movie_detail_screen_test.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update _pauseTrailer
    old_pause = """  Future<void> _pauseTrailer() async {
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
    new_pause = """  Future<void> _pauseTrailer() async {
    _userPausedTrailer = true;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript("window.dartShouldPause = true; if(typeof player !== 'undefined' && player && player.pauseVideo) { player.pauseVideo(); }");
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
    c = c.replace(old_pause, new_pause)

    # 2. Update _playTrailer
    old_play = """  void _playTrailer() async {
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
    new_play = """  void _playTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript("if(typeof player !== 'undefined' && player && player.playVideo) { player.playVideo(); }");
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
    c = c.replace(old_play, new_play)

    # 3. Update _resumeTrailer
    old_resume = """  void _resumeTrailer() async {
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
    new_resume = """  void _resumeTrailer() async {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript("if(typeof player !== 'undefined' && player && player.playVideo) { player.playVideo(); }");
      } catch (e) {}
      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
          _isTrailerPaused = false;
        });
      }
    }
  }"""
    c = c.replace(old_resume, new_resume)

    # 4. Add _isInitializingWebview guard
    if "bool _isInitializingWebview = false;" not in c:
        c = c.replace("bool _isWebviewInitialized = false;", "bool _isWebviewInitialized = false;\n  bool _isInitializingWebview = false;")
    
    old_start = """  void _startInlineTrailer() async {
    if (_movie == null || _movie!.trailerUrl == null || _movie!.trailerUrl!.isEmpty) return;

    final ytKey = _movie!.trailerUrl!.split('v=').last;"""
    new_start = """  void _startInlineTrailer() async {
    if (_movie == null || _movie!.trailerUrl == null || _movie!.trailerUrl!.isEmpty) return;
    if (_isInitializingWebview) return;
    _isInitializingWebview = true;

    final ytKey = _movie!.trailerUrl!.split('v=').last;"""
    c = c.replace(old_start, new_start)

    old_start_end = """      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
        });
      }
    }
  }"""
    new_start_end = """      if (mounted) {
        setState(() {
          _showInlineTrailer = true;
        });
      }
    }
    _isInitializingWebview = false;
  }"""
    c = c.replace(old_start_end, new_start_end)


    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Safely replaced JS logic!")
