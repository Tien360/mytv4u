import sys

code = """import 'dart:async';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

import '../api/youtube_game_api.dart';
import '../models/movie.dart';
import '../widgets/ambient_background.dart';
import '../widgets/glass_container.dart';
import '../utils/l10n.dart';
import 'player_screen.dart';

class GameDetailScreen extends StatefulWidget {
  final String gameUrl;
  final String gameTitle;
  final String initialThumb;

  const GameDetailScreen({
    Key? key,
    required this.gameUrl,
    required this.gameTitle,
    required this.initialThumb,
  }) : super(key: key);

  @override
  State<GameDetailScreen> createState() => _GameDetailScreenState();
}

class _GameDetailScreenState extends State<GameDetailScreen> {
  YoutubeGameInfo? _gameInfo;
  bool _isLoading = true;
  SharedPreferences? _prefs;
  bool _isYtLinked = false;
  bool _isHoveringPlay = false;

  @override
  void initState() {
    super.initState();
    _initData();
  }

  Future<void> _initData() async {
    _prefs = await SharedPreferences.getInstance();
    setState(() {
      _isYtLinked = _prefs?.getBool('is_yt_linked') ?? false;
    });

    final info = await YoutubeGameApi.fetchGameInfo(widget.gameUrl);
    if (mounted) {
      setState(() {
        _gameInfo = info;
        _isLoading = false;
      });
    }
  }

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
                    _launchGame();
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

  void _launchGame() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PlayerScreen(
          movieName: _gameInfo?.title ?? widget.gameTitle,
          episodes: [
            Episode(
              name: _gameInfo?.title ?? widget.gameTitle,
              slug: 'game',
              m3u8Url: '',
              embedUrl: widget.gameUrl,
            )
          ],
          currentEpisodeIndex: 0,
          isLive: true,
        ),
      ),
    );
  }

  void _onPlayTap() {
    if (_isYtLinked) {
      _launchGame();
    } else {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          backgroundColor: const Color(0xFF1E1E1E),
          title: const Text('Yêu cầu Đăng nhập', style: TextStyle(color: Colors.white)),
          content: const Text(
            'Để lưu tiến trình chơi game trên đám mây, bạn cần đăng nhập tài khoản Google (dùng chung cho YouTube).\\n\\nBạn có muốn đăng nhập ngay không?',
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
                _openYoutubeLogin();
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
    final String currentThumb = _gameInfo?.thumbUrl.isNotEmpty == true 
        ? _gameInfo!.thumbUrl 
        : widget.initialThumb;
        
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Ambient Background
          AmbientBackground(imageUrl: currentThumb),
          
          // Main Content
          SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 32),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Back Button
                  IconButton(
                    icon: const Icon(Icons.arrow_back_ios, color: Colors.white),
                    onPressed: () => Navigator.pop(context),
                  ),
                  const SizedBox(height: 24),
                  
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Poster
                      Hero(
                        tag: widget.gameUrl,
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(24),
                          child: CachedNetworkImage(
                            imageUrl: currentThumb,
                            width: 300,
                            height: 300,
                            fit: BoxFit.cover,
                            placeholder: (context, url) => Container(
                              width: 300,
                              height: 300,
                              color: Colors.white10,
                              child: const Center(child: CircularProgressIndicator()),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 48),
                      
                      // Details
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _gameInfo?.title ?? widget.gameTitle,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 48,
                                fontWeight: FontWeight.bold,
                                shadows: [Shadow(color: Colors.black54, blurRadius: 10)],
                              ),
                            ),
                            const SizedBox(height: 16),
                            
                            if (_isLoading)
                              const CircularProgressIndicator(color: Colors.white)
                            else if (_gameInfo != null) ...[
                              // Tags
                              Row(
                                children: [
                                  if (_gameInfo!.genre.isNotEmpty)
                                    _buildTag(_gameInfo!.genre, Colors.blueAccent),
                                  if (_gameInfo!.publisher.isNotEmpty) ...[
                                    const SizedBox(width: 8),
                                    _buildTag(_gameInfo!.publisher, Colors.purpleAccent),
                                  ]
                                ],
                              ),
                              const SizedBox(height: 24),
                              
                              // Info Row
                              Text(
                                'Ngày phát hành: ${_gameInfo!.releaseDate.isNotEmpty ? _gameInfo!.releaseDate : "Đang cập nhật"}',
                                style: const TextStyle(color: Colors.white70, fontSize: 16),
                              ),
                              if (_gameInfo!.developer.isNotEmpty) ...[
                                const SizedBox(height: 4),
                                Text(
                                  'Nhà phát triển: ${_gameInfo!.developer}',
                                  style: const TextStyle(color: Colors.white70, fontSize: 16),
                                ),
                              ],
                              const SizedBox(height: 32),
                              
                              // Description
                              Text(
                                _gameInfo!.description,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                  height: 1.5,
                                ),
                              ),
                            ],
                            
                            const SizedBox(height: 48),
                            
                            // Play Button
                            MouseRegion(
                              onEnter: (_) => setState(() => _isHoveringPlay = true),
                              onExit: (_) => setState(() => _isHoveringPlay = false),
                              cursor: SystemMouseCursors.click,
                              child: GestureDetector(
                                onTap: _onPlayTap,
                                child: AnimatedScale(
                                  scale: _isHoveringPlay ? 1.05 : 1.0,
                                  duration: const Duration(milliseconds: 200),
                                  child: GlassContainer(
                                    borderRadius: 30,
                                    padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 16),
                                    color: _isHoveringPlay ? Colors.redAccent.withOpacity(0.9) : Colors.redAccent.withOpacity(0.7),
                                    child: const Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Icon(Icons.play_arrow, color: Colors.white, size: 32),
                                        SizedBox(width: 12),
                                        Text(
                                          'CHƠI NGAY',
                                          style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 24,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTag(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Text(
        text,
        style: TextStyle(color: color, fontWeight: FontWeight.bold),
      ),
    );
  }
}
"""
with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print("Created game_detail_screen.dart")
