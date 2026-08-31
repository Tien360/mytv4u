import 'package:flutter/material.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:flutter/services.dart';

class GamePlayerScreen extends StatefulWidget {
  final String gameUrl;
  final String gameThumb;
  
  const GamePlayerScreen({
    Key? key,
    required this.gameUrl,
    required this.gameThumb,
  }) : super(key: key);

  @override
  State<GamePlayerScreen> createState() => _GamePlayerScreenState();
}

class _GamePlayerScreenState extends State<GamePlayerScreen> {
  final _controller = WebviewController();
  bool _isWebviewInitialized = false;
  bool _isGameReady = false;

  @override
  void initState() {
    super.initState();
    _initWebview();
  }

  Future<void> _initWebview() async {
    try {
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.black);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      
      _controller.webMessage.listen((message) {
        if (message == "game_ready") {
          if (mounted) {
            setState(() {
              _isGameReady = true;
            });
          }
        }
      });
      
      _controller.url.listen((url) async {
        if (url.contains("playables")) {
           await _injectFullscreenScript();
        }
      });
      
      await _controller.loadUrl(widget.gameUrl);

      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }
    } catch (e) {
      debugPrint("Game webview init error: $e");
    }
  }
  
  Future<void> _injectFullscreenScript() async {
    const js = '''
      let maximizeAttempts = 0;
      const makeFullscreen = () => {
          maximizeAttempts++;
          // YouTube playables are usually inside a specific tag or iframe
          let gameRenderer = document.querySelector('ytd-playable-game-renderer') || document.querySelector('iframe');
          if (gameRenderer) {
              gameRenderer.style.position = 'fixed';
              gameRenderer.style.top = '0';
              gameRenderer.style.left = '0';
              gameRenderer.style.width = '100vw';
              gameRenderer.style.height = '100vh';
              gameRenderer.style.zIndex = '999999';
              
              if(gameRenderer.tagName === 'IFRAME') {
                 gameRenderer.style.border = 'none';
              }
              document.body.style.overflow = 'hidden';
              
              // Hide everything else by hiding the page manager
              let app = document.querySelector('ytd-app');
              if(app) {
                 let masthead = document.querySelector('#masthead-container');
                 if(masthead) masthead.style.display = 'none';
              }
              
              window.chrome.webview.postMessage("game_ready");
          } else if (maximizeAttempts < 10) {
              setTimeout(makeFullscreen, 1000);
          }
      };
      setTimeout(makeFullscreen, 1000);
    ''';
    try {
      await _controller.executeScript(js);
    } catch(e) {}
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          if (_isWebviewInitialized)
            Webview(_controller),
            
          // Loading Overlay
          AnimatedOpacity(
            opacity: _isGameReady ? 0.0 : 1.0,
            duration: const Duration(milliseconds: 500),
            child: Container(
              color: Colors.black,
              width: double.infinity,
              height: double.infinity,
              child: Stack(
                alignment: Alignment.center,
                children: [
                   if (widget.gameThumb.isNotEmpty)
                     Opacity(
                       opacity: 0.3,
                       child: Image.network(
                         widget.gameThumb,
                         width: double.infinity,
                         height: double.infinity,
                         fit: BoxFit.cover,
                       ),
                     ),
                   Column(
                     mainAxisSize: MainAxisSize.min,
                     children: [
                       if (widget.gameThumb.isNotEmpty)
                         ClipRRect(
                           borderRadius: BorderRadius.circular(24),
                           child: Image.network(
                             widget.gameThumb,
                             width: 150,
                             height: 150,
                             fit: BoxFit.cover,
                           ),
                         ),
                       const SizedBox(height: 30),
                       const CircularProgressIndicator(color: Colors.redAccent),
                       const SizedBox(height: 16),
                       const Text(
                         'Đang khởi động trò chơi...',
                         style: TextStyle(color: Colors.white, fontSize: 18),
                       )
                     ],
                   )
                ],
              ),
            ),
          ),
          
          // Back Button always on top
          Positioned(
            top: 20,
            left: 20,
            child: IconButton(
              icon: const Icon(Icons.arrow_back_ios, color: Colors.white, shadows: [Shadow(color: Colors.black, blurRadius: 4)]),
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ],
      ),
    );
  }
}
