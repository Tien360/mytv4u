import codecs

with codecs.open('lib/screens/tv_player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Rename classes
code = code.replace("class PlayerScreen extends StatefulWidget", "class TvPlayerScreen extends StatefulWidget")
code = code.replace("const PlayerScreen({", "const TvPlayerScreen({")
code = code.replace("State<PlayerScreen> createState() => _PlayerScreenState();", "State<TvPlayerScreen> createState() => _TvPlayerScreenState();")
code = code.replace("class _PlayerScreenState extends State<PlayerScreen>", "class _TvPlayerScreenState extends State<TvPlayerScreen>")

# 2. Add DRM fields after _isUsingWebview
code = code.replace(
    "  bool _isUsingWebview = false;\n  bool _autoDetectedLive = false;",
    "  bool _isUsingWebview = false;\n  HttpServer? _localServer;\n  int _localPort = 0;\n  String _currentDrmKeys = '';\n  String _currentActualUrl = '';\n\n  bool _autoDetectedLive = false;"
)

# 3. Add _initLocalServer + call in initState
init_server_method = '''  Future<void> _initLocalServer() async {
    try {
      _localServer = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
      _localPort = _localServer!.port;
      _localServer!.listen((HttpRequest request) {
        if (request.uri.path == '/play.html') {
          final html = \\'\\'\\'<!DOCTYPE html>
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
        const manifestUri = \\'${_currentActualUrl}\\';
        const clearKeyConfig = ${_currentDrmKeys.isNotEmpty ? _currentDrmKeys : \\'{}\\'};
        async function init() {
            const video = document.getElementById(\\'video\\');
            const player = new shaka.Player(video);
            if (Object.keys(clearKeyConfig).length > 0) {
                player.configure({ drm: { clearKeys: clearKeyConfig } });
            }
            try { await player.load(manifestUri); } catch (e) { console.error(\\'Error\\', e); }
        }
        document.addEventListener(\\'DOMContentLoaded\\', init);
    </script>
</body>
</html>\\'\\'\\';
          request.response
            ..statusCode = HttpStatus.ok
            ..headers.contentType = ContentType.html
            ..write(html)
            ..close();
        }
      });
    } catch (e) {
      debugPrint("Local server error: \\$e");
    }
  }

'''
code = code.replace("  @override\n  void initState() {\n    super.initState();", init_server_method + "  @override\n  void initState() {\n    super.initState();\n    _initLocalServer();")

# 4. Add DRM parsing in _playCurrentUrl
old_play = '''  Future<void> _playCurrentUrl(Episode ep) async {
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
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));'''
new_play = '''  Future<void> _playCurrentUrl(Episode ep) async {
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
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty)));'''
code = code.replace(old_play, new_play)

# 5. Replace args URL and webview loadUrl
code = code.replace(
    "          List<String> args = [\n            _currentUrl,\n            title,",
    "          String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;\n          List<String> args = [\n            targetUrl,\n            title,"
)
code = code.replace(
    "      await _webController.loadUrl(_currentUrl);",
    "      String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;\n      await _webController.loadUrl(targetUrl);"
)

# 6. Add player.stop() before Navigator.pop in back button
code = code.replace(
    "                                    await player.stop();\n                                    if (mounted) Navigator.pop(context);",
    "                                    await player.stop();\n                                    if (mounted) Navigator.pop(context);"
)

# 7. Close local server in dispose
code = code.replace(
    "  @override\n  void dispose() {\n    windowManager.removeListener(this);",
    "  @override\n  void dispose() {\n    _localServer?.close();\n    windowManager.removeListener(this);"
)

with codecs.open('lib/screens/tv_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("TvPlayerScreen created successfully!")
