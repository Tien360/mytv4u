import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Add _userPausedTrailer variable
text = re.sub(r'(bool _showInlineTrailer = false;)', r'\1\n  bool _userPausedTrailer = false;', text)

# Fix _initWebview
old_init = '''      final url = 'http://127.0.0.1:/trailer.html';
      await _webviewController.loadUrl(url);

      if (mounted) {'''
new_init = '''      final url = 'http://127.0.0.1:/trailer.html';
      await _webviewController.loadUrl(url);

      if (_userPausedTrailer) {
        await _webviewController.executeScript("window.dartShouldPause = true;");
      }

      if (mounted) {'''
text = text.replace(old_init, new_init)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated declaration and init logic!")
