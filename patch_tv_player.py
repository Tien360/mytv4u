import codecs
import re

with codecs.open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Rename class
code = code.replace("class PlayerScreen extends StatefulWidget", "class TvPlayerScreen extends StatefulWidget")
code = code.replace("const PlayerScreen({", "const TvPlayerScreen({")
code = code.replace("State<PlayerScreen> createState() => _PlayerScreenState();", "State<TvPlayerScreen> createState() => _TvPlayerScreenState();")
code = code.replace("class _PlayerScreenState extends State<PlayerScreen>", "class _TvPlayerScreenState extends State<TvPlayerScreen>")

# 2. Add DRM Server fields
fields_block = """  bool _autoDetectedLive = false;
  bool _isExternalPlayerActive = false;
  SidePanelMode _activePanel = SidePanelMode.none;

  // TV DRM
  HttpServer? _localServer;
  int _localPort = 0;
  String _currentDrmKeys = '';
  String _currentActualUrl = '';
"""
code = re.sub(r'  bool _autoDetectedLive = false;\r?\n  bool _isExternalPlayerActive = false;\r?\n  SidePanelMode _activePanel = SidePanelMode\.none;', fields_block, code)

# 3. Add _initLocalServer
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
    <title>MyTV4U TV Player</title>
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

  @override
  void initState() {"""
code = code.replace("  @override\n  void initState() {", init_server)
code = code.replace("super.initState();", "super.initState();\n    _initLocalServer();")

# 4. Patch _playCurrentUrl to include DRM logic
old_play = """  Future<void> _playCurrentUrl(Episode ep) async {
    bool isVideoFile =
        _currentUrl.contains('.m3u8') || 
        _currentUrl.contains('.mp4') || 
        _currentUrl.contains('.flv') || 
        _currentUrl.contains('.mkv') || 
        _currentUrl.contains('proxy.php');
    
    _isUsingWebview =
        !isVideoFile &&
        _currentUrl.startsWith('http') &&
        (_currentUrl.contains('embed') ||
            _currentUrl.contains('player') ||
            _currentUrl.contains('iframe') ||
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));"""

new_play = """  Future<void> _playCurrentUrl(Episode ep) async {
    _currentActualUrl = _currentUrl;
    _currentDrmKeys = '';
    if (_currentUrl.contains('|drm:')) {
       final parts = _currentUrl.split('|drm:');
       _currentActualUrl = parts[0];
       _currentDrmKeys = parts[1];
    }

    bool isVideoFile =
        _currentActualUrl.contains('.m3u8') || 
        _currentActualUrl.contains('.mp4') || 
        _currentActualUrl.contains('.flv') || 
        _currentActualUrl.contains('.mkv') || 
        _currentActualUrl.contains('proxy.php');
    
    bool requiresDrm = _currentDrmKeys.isNotEmpty;

    _isUsingWebview =
        requiresDrm ||
        (!isVideoFile &&
        _currentActualUrl.startsWith('http') &&
        (_currentActualUrl.contains('embed') ||
            _currentActualUrl.contains('player') ||
            _currentActualUrl.contains('iframe') ||
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty)));"""
code = code.replace(old_play, new_play)

# 5. Patch targetUrl for args and webview
old_args = """          List<String> args = [
            _currentUrl,
            title,"""
new_args = """          String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
          List<String> args = [
            targetUrl,
            title,"""
code = code.replace(old_args, new_args)

code = code.replace("await _webController.loadUrl(_currentUrl);", "String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;\n      await _webController.loadUrl(targetUrl);")

# 6. Dispose local server
code = code.replace("  @override\n  void dispose() {", "  @override\n  void dispose() {\n    _localServer?.close();")

with codecs.open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Created TvPlayerScreen!")
