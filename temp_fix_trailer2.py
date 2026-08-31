import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        if (mounted) {
          setState(() {
            _isWebviewInitialized = true;
          });
        }"""

new_logic = """        if (mounted) {
          setState(() {
            _isWebviewInitialized = true;
          });
          if (_userPausedTrailer) {
            _webviewController.executeScript(
              "window.dartShouldPause = true; if(typeof player !== 'undefined' && player && player.pauseVideo) { player.pauseVideo(); }"
            );
          }
        }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed _initWebview")
else:
    print("Could not find old_logic")
