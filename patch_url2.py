import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

old_url = """          String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
          List<String> args = [
            targetUrl,
            title,
            bounds.left.toInt().toString(),"""
new_url = """          List<String> args = [
            _currentUrl,
            title,
            bounds.left.toInt().toString(),"""
code = code.replace(old_url, new_url)

old_web = """      String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
      await _webController.loadUrl(targetUrl);"""
new_web = """      await _webController.loadUrl(_currentUrl);"""
code = code.replace(old_web, new_web)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Restored web view urls")
