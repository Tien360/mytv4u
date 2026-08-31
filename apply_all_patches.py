import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Revert auto HW fallback
old_hw = """        player.stream.error.listen((error) {
          if (mounted) {
            String errStr = error.toString();
            if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
              return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
            }
            if (errStr.toLowerCase().contains('error decoding')) {
              if (_hwAccel) {
                _toggleHwAccel(false);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Phát hiện lỗi phần cứng, đang chuyển sang giải mã bằng phần mềm...'),
                    backgroundColor: Colors.orange,
                    duration: Duration(seconds: 3),
                  ),
                );
                return;
              } else {
                return; // Ignore if already SW decoding
              }
            }
            if (_tryFallbackDomain()) return;
            setState(() => errorMsg = errStr);
          }
        }),"""
new_hw = """        player.stream.error.listen((error) {
          if (mounted) {
            String errStr = error.toString();
            if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
              return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
            }
            if (_tryFallbackDomain()) return;
            setState(() => errorMsg = errStr);
          }
        }),"""
code = code.replace(old_hw, new_hw)

# 2. Add fields
fields = """  bool _isUsingWebview = false;
  HttpServer? _localServer;
  int _localPort = 0;
  String _currentDrmKeys = '';
  String _currentActualUrl = '';"""
code = code.replace("  bool _isUsingWebview = false;", fields)

# 3. Add _initLocalServer and call it in initState
init_func = """  Future<void> _initLocalServer() async {
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

  @override
  void initState() {"""

code = code.replace("  @override\n  void initState() {", init_func)
code = code.replace("super.initState();", "super.initState();\n    _initLocalServer();")

# 4. Patch _playCurrentUrl
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

# 5. Patch targetUrl
old_url = """          List<String> args = [
            _currentUrl,
            title,
            bounds.left.toInt().toString(),"""
new_url = """          String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
          List<String> args = [
            targetUrl,
            title,
            bounds.left.toInt().toString(),"""
code = code.replace(old_url, new_url)

old_web = """      await _webController.loadUrl(_currentUrl);"""
new_web = """      String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;
      await _webController.loadUrl(targetUrl);"""
code = code.replace(old_web, new_web)

# 6. Dispose local server
old_dispose = """  @override
  void dispose() {
    _sleepTimer?.cancel();"""
new_dispose = """  @override
  void dispose() {
    _localServer?.close();
    _sleepTimer?.cancel();"""
code = code.replace(old_dispose, new_dispose)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("All patches applied.")
