import os

with open("lib/screens/tv_webview_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace class names
content = content.replace("TvWebViewScreen", "GameWebViewScreen")
content = content.replace("tv360_webview_player", "game_webview_player")
content = content.replace("Trình phát WebView TV360", "Trình phát Game WebView")

# Add PathProvider import if not exists
if "import 'package:path_provider/path_provider.dart';" not in content:
    content = content.replace("import 'package:webview_windows/webview_windows.dart';", "import 'package:webview_windows/webview_windows.dart';\nimport 'package:path_provider/path_provider.dart';\nimport 'package:path/path.dart' as p;")

# Modify _initWebView to inject youtube_webview_profile
old_init = """  Future<void> _initWebView() async {
    try {
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.transparent);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl(widget.webUrl);"""

new_init = """  Future<void> _initWebView() async {
    try {
      final appDataDir = await getApplicationSupportDirectory();
      final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
      try {
        await WebviewController.initializeEnvironment(userDataPath: profileDir);
      } catch (e) {
        // Environment already initialized
      }
      
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.black);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl(widget.webUrl);"""

content = content.replace(old_init, new_init)

with open("lib/screens/game_webview_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Created game_webview_screen.dart")
