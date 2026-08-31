import codecs

with codecs.open('lib/screens/player_screen.dart', 'rb') as f:
    code = f.read().decode('utf-8')

# 1. Rename classes
code = code.replace('class PlayerScreen extends StatefulWidget', 'class TvPlayerScreen extends StatefulWidget')
code = code.replace('const PlayerScreen({', 'const TvPlayerScreen({')
code = code.replace('State<PlayerScreen> createState() => _PlayerScreenState();', 'State<TvPlayerScreen> createState() => _TvPlayerScreenState();')
code = code.replace('class _PlayerScreenState extends State<PlayerScreen>', 'class _TvPlayerScreenState extends State<TvPlayerScreen>')

# 2. Add DRM fields
code = code.replace(
    'bool _isUsingWebview = false;\r\n  bool _autoDetectedLive = false;',
    'bool _isUsingWebview = false;\r\n  HttpServer? _localServer;\r\n  int _localPort = 0;\r\n  String _currentDrmKeys = \'\';\r\n  String _currentActualUrl = \'\';\r\n\r\n  bool _autoDetectedLive = false;'
)

# 3. Add _initLocalServer + initState call
init_method = r'''  String _buildDrmHtml() {
    return '<!DOCTYPE html><html><head><meta charset="utf-8"><title>TV DRM</title>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.ui.min.js"></script>'
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/controls.min.css">'
        '<style>body,html{width:100%;height:100%;margin:0;padding:0;background:black;overflow:hidden}</style>'
        '</head><body>'
        '<div data-shaka-player-container style="width:100%;height:100%;">'
        '<video data-shaka-player id="video" style="width:100%;height:100%;" autoplay></video>'
        '</div>'
        '<script>'
        'const manifestUri="${_currentActualUrl}";'
        'const ck=${_currentDrmKeys.isNotEmpty ? _currentDrmKeys : "{}"};'
        'async function init(){'
        '  shaka.polyfill.installAll();'
        '  if(!shaka.Player.isBrowserSupported()){console.error("Browser not supported!");return;}'
        '  const video=document.getElementById("video");'
        '  const container=document.querySelector("[data-shaka-player-container]");'
        '  const player=new shaka.Player(video);'
        '  const ui=new shaka.ui.Overlay(player, container, video);'
        '  if(Object.keys(ck).length>0)player.configure({drm:{clearKeys:ck}});'
        '  try{'
        '    await player.load(manifestUri);'
        '    video.play().catch(e=>console.log("Autoplay prevented",e));'
        '  }catch(e){console.error(e);}'
        '}'
        'document.addEventListener("DOMContentLoaded",init);'
        '</script></body></html>';
  }

  Future<void> _initLocalServer() async {
    try {
      _localServer = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
      _localPort = _localServer!.port;
      _localServer!.listen((HttpRequest request) {
        if (request.uri.path == '/play.html') {
          request.response
            ..statusCode = HttpStatus.ok
            ..headers.contentType = ContentType.html
            ..write(_buildDrmHtml())
            ..close();
        }
      });
    } catch (e) {
      debugPrint("Local server error: $e");
    }
  }

'''

code = code.replace(
    '  @override\r\n  void initState() {\r\n    super.initState();',
    init_method + '  @override\r\n  void initState() {\r\n    super.initState();\r\n    _initLocalServer();'
)

# 4. Patch _playCurrentUrl for DRM
old_play = (
    '  Future<void> _playCurrentUrl(Episode ep) async {\r\n'
    '    bool isVideoFile =\r\n'
    '        _currentUrl.contains(\'.m3u8\') || \r\n'
    '        _currentUrl.contains(\'.mp4\') || \r\n'
    '        _currentUrl.contains(\'.flv\') || \r\n'
    '        _currentUrl.contains(\'.mkv\') || \r\n'
    '        _currentUrl.contains(\'proxy.php\');\r\n'
    '    _isUsingWebview =\r\n'
    '        !isVideoFile &&\r\n'
    '        _currentUrl.startsWith(\'http\') &&\r\n'
    '        (_currentUrl.contains(\'embed\') ||\r\n'
    '            _currentUrl.contains(\'player\') ||\r\n'
    '            _currentUrl.contains(\'iframe\') ||\r\n'
    '            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));'
)
new_play = (
    '  Future<void> _playCurrentUrl(Episode ep) async {\r\n'
    '    _currentActualUrl = _currentUrl;\r\n'
    '    _currentDrmKeys = \'\';\r\n'
    '    if (_currentUrl.contains(\'|drm:\')) {\r\n'
    '       final parts = _currentUrl.split(\'|drm:\');\r\n'
    '       _currentActualUrl = parts[0];\r\n'
    '       _currentDrmKeys = parts[1];\r\n'
    '    }\r\n'
    '\r\n'
    '    bool isVideoFile =\r\n'
    '        _currentActualUrl.contains(\'.m3u8\') || \r\n'
    '        _currentActualUrl.contains(\'.mp4\') || \r\n'
    '        _currentActualUrl.contains(\'.flv\') || \r\n'
    '        _currentActualUrl.contains(\'.mkv\') || \r\n'
    '        _currentActualUrl.contains(\'proxy.php\');\r\n'
    '    \r\n'
    '    bool requiresDrm = _currentDrmKeys.isNotEmpty;\r\n'
    '\r\n'
    '    _isUsingWebview =\r\n'
    '        requiresDrm ||\r\n'
    '        (!isVideoFile &&\r\n'
    '        _currentActualUrl.startsWith(\'http\') &&\r\n'
    '        (_currentActualUrl.contains(\'embed\') ||\r\n'
    '            _currentActualUrl.contains(\'player\') ||\r\n'
    '            _currentActualUrl.contains(\'iframe\') ||\r\n'
    '            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty)));'
)
if old_play in code:
    code = code.replace(old_play, new_play)
    print("DRM _playCurrentUrl patched OK")
else:
    print("ERROR: DRM _playCurrentUrl NOT FOUND")

# 5. Patch external player args
old_args = '          List<String> args = [\r\n            _currentUrl,\r\n            title,'
new_args = "          String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;\r\n          List<String> args = [\r\n            targetUrl,\r\n            title,"
if old_args in code:
    code = code.replace(old_args, new_args)
    print("Args patched OK")
else:
    print("ERROR: Args NOT FOUND")

# 6. Patch inline webview loadUrl
old_web = '      await _webController.loadUrl(_currentUrl);'
new_web = "      String targetUrl = requiresDrm ? 'http://127.0.0.1:$_localPort/play.html?t=${DateTime.now().millisecondsSinceEpoch}' : _currentActualUrl;\r\n      await _webController.loadUrl(targetUrl);"
if old_web in code:
    code = code.replace(old_web, new_web)
    print("WebView loadUrl patched OK")
else:
    print("ERROR: WebView NOT FOUND")

# 7. Close local server in dispose
code = code.replace(
    '  @override\r\n  void dispose() {\r\n    windowManager.removeListener(this);',
    '  @override\r\n  void dispose() {\r\n    _localServer?.close();\r\n    windowManager.removeListener(this);'
)

with codecs.open('lib/screens/tv_player_screen.dart', 'wb') as f:
    f.write(code.encode('utf-8'))

print("ALL DONE!")
