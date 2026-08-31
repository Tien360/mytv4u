import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# Update _webController.loadUrl
old_loadUrl = """        _webController.containsFullScreenElementChanged.listen((flag) async {
          if (mounted) {
            setState(() {
              _isFullscreen = flag;
            });
            await windowManager.setFullScreen(flag);
          }
        });

        _isWebviewInitialized = true;
      }
      await _webController.loadUrl(_currentUrl);
      if (mounted) setState(() {});
    } else {"""

new_loadUrl = """        _webController.containsFullScreenElementChanged.listen((flag) async {
          if (mounted) {
            setState(() {
              _isFullscreen = flag;
            });
            await windowManager.setFullScreen(flag);
          }
        });

        _isWebviewInitialized = true;
      }
      String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
      await _webController.loadUrl(targetUrl);
      if (mounted) setState(() {});
    } else {"""

code = code.replace(old_loadUrl, new_loadUrl)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched webController.loadUrl")
