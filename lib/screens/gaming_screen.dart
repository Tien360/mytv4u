import 'dart:async';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import '../widgets/glass_container.dart';
import '../utils/l10n.dart';
import 'game_webview_screen.dart';

class GamingScreen extends StatefulWidget {
  const GamingScreen({Key? key}) : super(key: key);

  @override
  State<GamingScreen> createState() => _GamingScreenState();
}

class _GamingScreenState extends State<GamingScreen> {
  SharedPreferences? _prefs;
  bool _isYtLinked = false;

  final List<Map<String, String>> _games = [
    {
      'title': 'Stealth Master',
      'url': 'https://www.youtube.com/playables/UgkxAa2Gygx3bQRx4kOraVwUFW_3mO1tH0h5',
      'image': 'https://play-lh.googleusercontent.com/D4s3L2P-uA6l2Qh6bTz7H2lXq7S1j-K3J_Y5_8T-M0D0sM-s1QZ0Y-7L0X0B_6F2W2U=w512-h512',
    }
  ];

  @override
  void initState() {
    super.initState();
    _initPrefs();
  }

  Future<void> _initPrefs() async {
    _prefs = await SharedPreferences.getInstance();
    setState(() {
      _isYtLinked = _prefs?.getBool('is_yt_linked') ?? false;
    });
  }

  Future<void> _openYoutubeLogin(String gameUrl, String gameTitle) async {
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
                    // Launch game after successful login
                    _launchGame(gameUrl, gameTitle);
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
                          Text('Đăng nhập YouTube (Bắt buộc để lưu Game)', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
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

  void _launchGame(String url, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GameWebViewScreen(title: title, webUrl: url),
      ),
    );
  }

  void _onGameTap(String url, String title) {
    if (_isYtLinked) {
      _launchGame(url, title);
    } else {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          backgroundColor: const Color(0xFF1E1E1E),
          title: const Text('Yêu cầu Đăng nhập', style: TextStyle(color: Colors.white)),
          content: const Text(
            'Để lưu tiến trình chơi game trên đám mây, bạn cần đăng nhập tài khoản Google (dùng chung cho YouTube).\n\nBạn có muốn đăng nhập ngay không?',
            style: TextStyle(color: Colors.white70),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Hủy', style: TextStyle(color: Colors.white54)),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              onPressed: () {
                Navigator.pop(context);
                _openYoutubeLogin(url, title);
              },
              child: const Text('Đăng nhập', style: TextStyle(color: Colors.white)),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            L10n.t('nav_gaming') ?? 'Trò chơi (YouTube Playables)',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.0,
              ),
              itemCount: _games.length,
              itemBuilder: (context, index) {
                final game = _games[index];
                return GestureDetector(
                  onTap: () => _onGameTap(game['url']!, game['title']!),
                  child: GlassContainer(
                    borderRadius: 16,
                    padding: const EdgeInsets.all(0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Expanded(
                          child: ClipRRect(
                            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                            child: Image.network(
                              game['image']!,
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.all(12),
                          color: Colors.black45,
                          child: Text(
                            game['title']!,
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
