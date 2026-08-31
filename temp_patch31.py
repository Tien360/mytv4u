import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

func = """  Future<void> _openYoutubeLogin() async {
    setState(() => _isLoggingIn = true);
    try {
      final String exePath = Platform.resolvedExecutable;
      final String exeName = File(exePath).uri.pathSegments.last.replaceAll('.exe', '');
      final String webviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';

      final webviewDir = Directory(webviewPath);
      if (webviewDir.existsSync()) {
        try {
          webviewDir.deleteSync(recursive: true);
        } catch (e) {}
      }
      
      final webview = WebviewController();
      await webview.initialize();
      await webview.clearCache();
      
      final prefs = await SharedPreferences.getInstance();

      final result = await showDialog(
        context: context,
        builder: (context) {
          return Dialog(
            backgroundColor: Colors.transparent,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: SizedBox(
                width: 800,
                height: 600,
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      color: Colors.black87,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Đăng nhập YouTube', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                          IconButton(icon: const Icon(Icons.close, color: Colors.white), onPressed: () => Navigator.pop(context)),
                        ],
                      ),
                    ),
                    Expanded(child: Webview(webview)),
                  ],
                ),
              ),
            ),
          );
        },
      );
    } catch (e) {
      debugPrint('WebView Error: $e');
    }
  }
"""

if "Future<void> _openYoutubeLogin" not in content:
    idx = content.find("  Widget _buildLoginCard")
    if idx != -1:
        content = content[:idx] + func + "\n" + content[idx:]
        print("Re-injected _openYoutubeLogin")
        with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print("Could not find _buildLoginCard")
else:
    print("Already in content")
