import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

init_server = """  Future<void> _initLocalServer() async {
    try {
      _localServer = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
      _localPort = _localServer!.port;
      _localServer!.listen((HttpRequest request) {
        if (request.uri.path == '/play.html') {
          final html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MyTV4U DRM Player</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.ui.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/controls.min.css">
    <style>body, html { width: 100%; height: 100%; margin: 0; padding: 0; background-color: black; overflow: hidden; }</style>
</head>
<body>
    <video id="video" width="100%" height="100%" autoplay></video>
    <script>
        const manifestUri = '${_currentActualUrl}';
        const clearKeyConfig = ${_currentDrmKeys.isNotEmpty ? _currentDrmKeys : '{}'};

        async function init() {
            const video = document.getElementById('video');
            const player = new shaka.Player(video);
            
            if (Object.keys(clearKeyConfig).length > 0) {
                player.configure({
                    drm: { clearKeys: clearKeyConfig }
                });
            }

            try {
                await player.load(manifestUri);
            } catch (e) {
                console.error('Error loading', e);
            }
        }
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>''';
          request.response
            ..statusCode = HttpStatus.ok
            ..headers.contentType = ContentType.html
            ..write(html)
            ..close();
        }
      });
    } catch (e) {
      debugPrint("Local server error: $e");
    }
  }

"""

# Insert right before void initState
code = code.replace("  @override\n  void initState() {", init_server + "  @override\n  void initState() {")

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Injected _initLocalServer")
