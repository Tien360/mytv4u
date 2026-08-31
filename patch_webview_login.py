import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import 'package:webview_windows/webview_windows.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;"""

if "webview_windows" not in content:
    content = content.replace("import 'package:shared_preferences/shared_preferences.dart';", "import 'package:shared_preferences/shared_preferences.dart';\n" + imports)

# 2. Add the method and the youtube card
method = """
  Future<void> _openYoutubeLogin() async {
    final _controller = WebviewController();
    
    final appDataDir = await getApplicationSupportDirectory();
    final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
    
    try {
      await _controller.initialize(userDataFolder: profileDir);
      await _controller.setBackgroundColor(Colors.transparent);
      await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
      await _controller.loadUrl('https://accounts.google.com/ServiceLogin?service=youtube&continue=https://www.youtube.com');
      
      if (!mounted) return;
      
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) {
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
                          Text('Trình duyệt Đăng nhập YouTube', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white),
                        onPressed: () {
                          _controller.dispose();
                          Navigator.pop(context);
                        },
                      )
                    ],
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Webview(_controller),
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Text('Đăng nhập thành công, bạn có thể đóng cửa sổ này.', style: TextStyle(color: Colors.white70, fontStyle: FontStyle.italic)),
                ],
              ),
            ),
          );
        }
      );
    } catch (e) {
      print('Webview init error: $e');
    }
  }

  Widget _buildYouTubeLinkCard() {
    return GlassContainer(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.smart_display, color: Colors.redAccent, size: 28),
              const SizedBox(width: 12),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Liên kết Tài khoản YouTube', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text('Sử dụng để xem các nội dung giới hạn độ tuổi và bỏ qua quảng cáo.', style: TextStyle(color: Colors.white54, fontSize: 13)),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              icon: const Icon(Icons.login, color: Colors.white),
              label: const Text('Mở Trình duyệt Ẩn để Đăng nhập YouTube', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.redAccent,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              onPressed: _openYoutubeLogin,
            ),
          ),
        ],
      ),
    );
  }
"""

if "_openYoutubeLogin" not in content:
    idx = content.find("Widget _buildUserCard()")
    content = content[:idx] + method + content[idx:]

inject_target = """                                  if (_currentUser != null)
                                    _buildUserCard()
                                  else
                                    _buildLoginCard(),"""

if "_buildYouTubeLinkCard()" not in content:
    content = content.replace(inject_target, inject_target + "\n\n                                  const SizedBox(height: 16),\n                                  _buildYouTubeLinkCard(),")


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected YouTube Link section successfully")
