import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"        if \(mounted\) \{\n          setState\(\(\) \{\n            _isWebviewInitialized = true;\n          \}\);\n        \}"
replacement = """        if (mounted) {
          setState(() {
            _isWebviewInitialized = true;
          });
          if (_userPausedTrailer) {
            _webviewController.executeScript(
              "window.dartShouldPause = true; if(typeof player !== 'undefined' && player && player.pauseVideo) { player.pauseVideo(); }"
            );
          }
        }"""

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed _initWebview with regex")
else:
    print("Could not find pattern")
