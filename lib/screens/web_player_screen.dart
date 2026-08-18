import 'dart:async';
import 'package:flutter/material.dart';
import 'package:webview_windows/webview_windows.dart';
import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:window_manager/window_manager.dart';

class WebPlayerScreen extends StatefulWidget {
  final String title;
  final String ytKey;

  const WebPlayerScreen({super.key, required this.title, required this.ytKey});

  @override
  State<WebPlayerScreen> createState() => _WebPlayerScreenState();
}

class _WebPlayerScreenState extends State<WebPlayerScreen> {
  final _controller = WebviewController();
  bool _isWebviewInitialized = false;
  HttpServer? _server;
  int _port = 0;
  bool _isFullscreen = false;

  @override
  void initState() {
    super.initState();
    _startServerAndInitWebview();
  }

  Future<void> _startServerAndInitWebview() async {
    _server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    _port = _server!.port;
    
    _server!.listen((HttpRequest request) {
      if (request.uri.path == '/trailer.html') {
        final videoId = request.uri.queryParameters['id'] ?? '';
        final html = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Trailer</title>
    <style>
      body, html { width: 100%; height: 100%; margin: 0; padding: 0; background-color: black; overflow: hidden; }
      #player { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; border: none; }
    </style>
  </head>
  <body>
    <div id="player"></div>
    <script>
      var tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      var player;
      function onYouTubeIframeAPIReady() {
        if (!'$videoId') return;
        player = new YT.Player('player', {
          height: '100%',
          width: '100%',
          videoId: '$videoId',
          playerVars: {
            'autoplay': 1,
            'rel': 0,
            'modestbranding': 1,
            'fs': 1,
            'iv_load_policy': 3,
            'controls': 1
          },
          events: {
            'onReady': function(event) {
              event.target.playVideo();
            }
          }
        });
      }
    </script>
  </body>
</html>
''';
        request.response
          ..headers.contentType = ContentType.html
          ..write(html)
          ..close();
      } else {
        request.response
          ..statusCode = HttpStatus.notFound
          ..close();
      }
    });

    try {
      await _controller.initialize();
      await _controller.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
      
      final url = 'http://127.0.0.1:$_port/trailer.html?id=${widget.ytKey}';
      await _controller.loadUrl(url);

      _controller.containsFullScreenElementChanged.listen((flag) async {
        if (mounted) {
          setState(() {
            _isFullscreen = flag;
          });
          await windowManager.setFullScreen(flag);
        }
      });

      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }
    } catch (e) {
      print('WebPlayerScreen Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: _isFullscreen ? null : AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: Text(widget.title, style: const TextStyle(color: Colors.white, fontSize: 16)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: _isWebviewInitialized
          ? Webview(_controller)
          : Center(child: CircularProgressIndicator()),
    );
  }

  @override
  void dispose() {
    _server?.close(force: true);
    _controller.dispose();
    super.dispose();
  }
}
