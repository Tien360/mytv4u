import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

if "import 'package:webview_windows/webview_windows.dart';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:webview_windows/webview_windows.dart';\nimport 'package:path/path.dart' as p;\nimport 'package:path_provider/path_provider.dart';\nimport 'dart:async';\nimport 'dart:io';")

# 1. Add _isYtLinked
if "bool _isYtLinked" not in content:
    content = content.replace("bool _easterEggsEnabled = true;", "bool _easterEggsEnabled = true;\n  bool _isYtLinked = false;")

# 2. Add _loadSettings loading
if "_isYtLinked = _prefs" not in content:
    content = content.replace("_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;", "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;\n    _isYtLinked = _prefs!.getBool('is_yt_linked') ?? false;")

# 3. Add Youtube Sync Card right after Firebase Sync
yt_card = """
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8),
            child: Divider(color: Colors.white10),
          ),
          // YouTube
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.play_circle_filled, color: _isYtLinked ? Colors.redAccent : Colors.grey, size: 20),
                  const SizedBox(width: 8),
                  Text(L10n.t('sync_yt') ?? 'YouTube (Gợi ý Cá nhân hóa)', style: TextStyle(color: _isYtLinked ? Colors.white : Colors.grey)),
                ],
              ),
              if (_isYtLinked)
                OutlinedButton(
                  onPressed: () async {
                    final prefs = await SharedPreferences.getInstance();
                    await prefs.setBool('is_yt_linked', false);
                    setState(() => _isYtLinked = false);
                    
                    try {
                      final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
                      final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
                      final dir = Directory(defaultWebviewPath);
                      if (dir.existsSync()) {
                        dir.deleteSync(recursive: true);
                      }
                    } catch (e) {
                      debugPrint('Failed to delete WebView data: $e');
                    }
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(L10n.t('yt_unlink_msg') ?? 'Đã ngắt kết nối YouTube')));
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.redAccent,
                    side: const BorderSide(color: Colors.redAccent),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: Text(L10n.t('btn_disconnect') ?? 'Ngắt kết nối', style: const TextStyle(fontSize: 12)),
                )
              else
                ElevatedButton(
                  onPressed: _openYoutubeLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: Text(L10n.t('btn_connect') ?? 'Kết nối', style: const TextStyle(fontSize: 12, color: Colors.white)),
                ),
            ],
          ),
"""

# We inject yt_card inside _buildUserCard and _buildLoginCard
if "// YouTube" not in content:
    # Inject into UserCard (before closing Column)
    user_card_end = content.find("              ],\n            ),\n          ),\n        ],\n      ),\n    );")
    if user_card_end != -1:
        content = content[:user_card_end] + yt_card + content[user_card_end:]
    
    # Inject into LoginCard (before closing Column)
    login_card_end = content.find("              ),\n            ),\n          ],\n        ),\n      );\n    }")
    if login_card_end != -1:
        content = content[:login_card_end] + yt_card + content[login_card_end:]

# 4. Add Optimizer Button before watch_limit
opt_card = """
                                  Container(
                                    width: double.infinity,
                                    margin: const EdgeInsets.only(bottom: 16),
                                    decoration: BoxDecoration(
                                      color: Colors.blueAccent.withOpacity(0.1),
                                      borderRadius: BorderRadius.circular(12),
                                      border: Border.all(color: Colors.blueAccent.withOpacity(0.3)),
                                    ),
                                    child: ListTile(
                                      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                                      leading: const Icon(Icons.speed, color: Colors.blueAccent, size: 32),
                                      title: Text(L10n.t('setting_opt_title') ?? 'Trợ lý Tối ưu hóa (Khuyên dùng)', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                                      subtitle: Text(L10n.t('setting_opt_desc') ?? 'Tự động quét cấu hình máy tính và thiết lập giao diện mượt mà nhất.', style: const TextStyle(color: Colors.white70)),
                                      trailing: ElevatedButton(
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.blueAccent,
                                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                        ),
                                        onPressed: () async {
                                          final result = await showDialog(context: context, builder: (_) => const OptimizerDialog());
                                          if (result != null) {
                                            _loadSettings(); // Reload if changed
                                          }
                                        },
                                        child: Text(L10n.t('setting_opt_btn') ?? 'Quét ngay', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                      ),
                                    ),
                                  ),
"""
if "Icons.speed" not in content:
    content = content.replace("                                      child: Column(\n                                        children: [\n                                          ListTile(", "                                      child: Column(\n                                        children: [\n" + opt_card + "\n                                          ListTile(")
    # Import OptimizerDialog
    if "import '../widgets/optimizer_dialog.dart';" not in content:
        content = content.replace("import '../widgets/custom_title_bar.dart';", "import '../widgets/custom_title_bar.dart';\nimport '../widgets/optimizer_dialog.dart';")

# 5. Add _openYoutubeLogin
yt_logic = """
  Future<void> _openYoutubeLogin() async {
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
          
          return Dialog(
            backgroundColor: const Color(0xFF1E1E1E),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Container(
              width: 800,
              height: 600,
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.security, color: Colors.green, size: 24),
                          SizedBox(width: 8),
                          Text('Đăng nhập YouTube', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white),
                        onPressed: () {
                          checkTimer?.cancel();
                          _controller.dispose();
                          Navigator.pop(context);
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: Webview(_controller),
                  ),
                ],
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

if "_openYoutubeLogin() async {" not in content:
    content = content.replace("  Widget _buildLoginCard() {", yt_logic + "\n\n  Widget _buildLoginCard() {")

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("SUCCESSFULLY PATCHED YOUTUBE AND OPTIMIZER!")
