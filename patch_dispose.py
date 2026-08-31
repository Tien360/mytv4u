import codecs

with codecs.open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

bad_str = """  void _toggleFullscreen() async {
    bool isFS = await windowManager.isFullScreen();
    await windowManager.setFullScreen(!isFS);
    _disposeMediaKit();
    if (_isWebviewInitialized) _webController.dispose();
    super.dispose();
  }"""
good_str = """  void _toggleFullscreen() async {
    bool isFS = await windowManager.isFullScreen();
    await windowManager.setFullScreen(!isFS);
    if (mounted) {
      setState(() => _isFullscreen = !isFS);
    }
  }

  @override
  void dispose() {
    _localServer?.close();
    windowManager.removeListener(this);
    _saveProgressTimer?.cancel();
    _saveLocalProgress();
    _focusNode.dispose();
    _hideControlsTimer?.cancel();
    _disposeMediaKit();
    if (_isWebviewInitialized) _webController.dispose();
    super.dispose();
  }"""
code = code.replace(bad_str, good_str)

with codecs.open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed the bad dispose replacement.")
