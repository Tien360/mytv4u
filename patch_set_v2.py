import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State changes
state_old = "String _ytCookieSource = 'none';"
state_new = "bool _isYtLinked = false;"
if "String _ytCookieSource" in content:
    content = content.replace(state_old, state_new)

load_old = "_ytCookieSource = _prefs!.getString('yt_cookie_source') ?? 'none';"
load_new = "_isYtLinked = _prefs!.getBool('is_yt_linked') ?? false;"
if "_ytCookieSource = _prefs!" in content:
    content = content.replace(load_old, load_new)

# 2. Add Timer to imports
if "import 'dart:async';" not in content:
    content = content.replace("import 'dart:io';", "import 'dart:io';\nimport 'dart:async';")

# 3. Modify _openYoutubeLogin
method_old = """  Future<void> _openYoutubeLogin() async {
    final _controller = WebviewController();
    
    final appDataDir = await getApplicationSupportDirectory();
    final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
    
    try {
      try {
        await WebviewController.initializeEnvironment(userDataPath: profileDir);
      } catch (e) {
        print('Environment already initialized: $e');
      }
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.transparent);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl('https://accounts.google.com/ServiceLogin?service=youtube&continue=https://www.youtube.com');
      
      if (!mounted) return;
      
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) {
          return Dialog("""

method_new = """  Future<void> _openYoutubeLogin() async {
    final _controller = WebviewController();
    Timer? checkTimer;
    
    final appDataDir = await getApplicationSupportDirectory();
    final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
    
    try {
      try {
        await WebviewController.initializeEnvironment(userDataPath: profileDir);
      } catch (e) {}
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.transparent);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl('https://accounts.google.com/ServiceLogin?service=youtube&continue=https://www.youtube.com');
      
      if (!mounted) return;
      
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) {
          
          if (checkTimer == null) {
            checkTimer = Timer.periodic(const Duration(seconds: 2), (t) async {
              try {
                if (_controller.value.isInitialized) {
                  final html = await _controller.executeScript("document.documentElement.innerHTML") as String?;
                  if (html != null && (html.contains('id="avatar-btn"') || html.contains('data-testid="account-menu-button"'))) {
                    t.cancel();
                    await _prefs!.setBool('is_yt_linked', true);
                    setState(() { _isYtLinked = true; });
                    if (Navigator.canPop(context)) Navigator.pop(context);
                  }
                }
              } catch (e) {}
            });
          }
          
          return Dialog("""

if "Timer? checkTimer;" not in content:
    content = content.replace(method_old, method_new)

# Add dispose logic to close button
close_old = """                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white),
                        onPressed: () {
                          _controller.dispose();
                          Navigator.pop(context);
                        },
                      )"""
close_new = """                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white),
                        onPressed: () {
                          checkTimer?.cancel();
                          _controller.dispose();
                          Navigator.pop(context);
                        },
                      )"""
content = content.replace(close_old, close_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched _openYoutubeLogin")
