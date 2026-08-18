import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add _userPausedTrailer flag
text = re.sub(r'(bool _showInlineTrailer = false;\s*bool _isTrailerPaused = false;)', 
              r'\1\n  bool _userPausedTrailer = false;', text)

# 2. Update _pauseTrailer
old_pause = '''  Future<void> _pauseTrailer() async {
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "if(player && player.pauseVideo) { player.pauseVideo(); }",
        );
      } catch (e) {}
    }'''

new_pause = '''  Future<void> _pauseTrailer() async {
    _userPausedTrailer = true;
    if (_isWebviewInitialized) {
      try {
        await _webviewController.executeScript(
          "window.dartShouldPause = true; if(typeof player !== 'undefined' && player && player.pauseVideo) { player.pauseVideo(); }",
        );
      } catch (e) {}
    }'''
text = text.replace(old_pause, new_pause)

# 3. Update _playTrailer
old_play = '''  void _playTrailer() {
    if (_isWebviewInitialized) {'''
new_play = '''  void _playTrailer() {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {'''
text = text.replace(old_play, new_play)

# 4. Update _resumeTrailer
old_resume = '''  void _resumeTrailer() {
    if (_isWebviewInitialized) {'''
new_resume = '''  void _resumeTrailer() {
    _userPausedTrailer = false;
    if (_isWebviewInitialized) {'''
text = text.replace(old_resume, new_resume)

# 5. Inject setInterval into HTML
old_html_script = '''        var player;
        function onYouTubeIframeAPIReady() {'''
new_html_script = '''        var player;
        window.dartShouldPause = false;
        setInterval(function() {
          if (window.dartShouldPause && typeof player !== 'undefined' && player && player.pauseVideo) {
            player.pauseVideo();
            window.dartShouldPause = false;
          }
        }, 500);
        function onYouTubeIframeAPIReady() {'''
text = text.replace(old_html_script, new_html_script)

# 6. Check _userPausedTrailer in _initWebview
old_init_end = '''      final url = 'http://127.0.0.1:/trailer.html';
      await _webviewController.loadUrl(url);

      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }
    } catch (e) {'''
new_init_end = '''      final url = 'http://127.0.0.1:/trailer.html';
      await _webviewController.loadUrl(url);

      if (_userPausedTrailer) {
        await _webviewController.executeScript("window.dartShouldPause = true;");
      }

      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }
    } catch (e) {'''
text = text.replace(old_init_end, new_init_end)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated movie_detail_screen.dart!")
