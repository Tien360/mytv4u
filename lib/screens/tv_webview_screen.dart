import 'package:flutter/material.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:window_manager/window_manager.dart';

class TvWebViewScreen extends StatefulWidget {
  final String title;
  final String webUrl;

  const TvWebViewScreen({Key? key, required this.title, required this.webUrl}) : super(key: key);

  @override
  State<TvWebViewScreen> createState() => _TvWebViewScreenState();
}

class _TvWebViewScreenState extends State<TvWebViewScreen> {
  final _controller = WebviewController();
  bool _isInitialized = false;
  String? _error;
  bool _isFullscreen = false;

  @override
  void initState() {
    super.initState();
    _initWebView();
  }

  Future<void> _initWebView() async {
    try {
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.black);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl(widget.webUrl);

      _controller.containsFullScreenElementChanged.listen((flag) async {
        if (mounted) {
          setState(() {
            _isFullscreen = flag;
          });
          await windowManager.setFullScreen(flag);
        }
      });

      _controller.loadingState.listen((state) async {
        if (state == LoadingState.navigationCompleted && mounted) {
          setState(() {
            _isInitialized = true;
            _isFullscreen = true;
          });
          await windowManager.setFullScreen(true);
          
          // Inject Javascript để ẩn giao diện thừa của trang web tinhlagi, chỉ giữ lại khung player
          await _controller.executeScript('''
            try {
              var style = document.createElement('style');
              style.innerHTML = `
                .nav-menu, .now-playing, .last-update, .group-title, .channel-grid, .search-container, .footer { display: none !important; }
                body, html, .container, .player-wrapper, .video-box { 
                  margin: 0 !important; 
                  padding: 0 !important; 
                  max-width: 100% !important; 
                  width: 100vw !important; 
                  height: 100vh !important; 
                  border-radius: 0 !important; 
                }
              `;
              document.head.appendChild(style);
              
              // Hide the "Kênh Trước / Kênh Sau" buttons which use inline flex
              var flexDivs = document.querySelectorAll('div[style*="display: flex"]');
              flexDivs.forEach(d => {
                if(d.innerHTML.includes('Kênh Trước') || d.innerHTML.includes('nav-btn')) d.style.display = 'none';
              });
            } catch(e) {}
          ''');
        }
      });
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = e.toString();
        });
      }
    }
  }

  @override
  void dispose() {
    windowManager.setFullScreen(false);
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: _isFullscreen ? null : AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.title,
              style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const Text(
              'Trình phát WebView TV360 Trực tiếp',
              style: TextStyle(color: Colors.blueAccent, fontSize: 12),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            tooltip: 'Tải lại trang',
            onPressed: () {
              if (_isInitialized) {
                _controller.reload();
              }
            },
          ),
        ],
      ),
      body: _error != null
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
                  const SizedBox(height: 12),
                  Text(
                    'Không thể tải WebView: $_error',
                    style: const TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            )
          : !_isInitialized
              ? const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CircularProgressIndicator(color: Colors.blue),
                      SizedBox(height: 16),
                      Text(
                        'Đang mở TV360 Web Player trong ứng dụng...',
                        style: TextStyle(color: Colors.white70),
                      ),
                    ],
                  ),
                )
              : Webview(_controller),
    );
  }
}

