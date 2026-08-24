import 'player_screen.dart';
import '../models/movie.dart';
import '../utils/l10n.dart';
import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import '../widgets/glass_container.dart';
import 'package:media_kit/media_kit.dart';
import 'main_screen.dart';
import 'movie_detail_screen.dart';
import '../widgets/custom_title_bar.dart';
import '../services/deep_link_service.dart';
import '../api/firebase_api.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late Player _player;
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();

    // Khởi tạo Player để phát âm thanh
    _player = Player();
    _player.open(Media('asset://assets/intro-sound.mp3'), play: true);
    _player.setVolume(50.0);

    // Khởi tạo Animation
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _scaleAnimation = Tween<double>(begin: 0.9, end: 1.1).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeOut),
    );

    _glowAnimation = Tween<double>(begin: 0.0, end: 20.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );

    _animationController.forward();

    _initializeApp();
  }

  Future<void> _initializeApp() async {
    final minWait = Future.delayed(const Duration(milliseconds: 2500));

    final status = await FirebaseApi.checkAppStatus();

    await minWait;

    if (!mounted) return;

    if (status['isKilled'] == true) {
      showDialog(
        context: context,
        barrierDismissible: false,
        barrierColor: Colors.black.withValues(alpha: 0.8),
        builder: (context) => WillPopScope(
          onWillPop: () async => false, // Chặn nút back
          child: Dialog(
            backgroundColor: Colors.transparent,
            elevation: 0,
            child: GlassContainer(
              width: 400,
              padding: const EdgeInsets.all(24),
              borderRadius: 24,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
                  const SizedBox(height: 16),
                  Text(
                    L10n.t('app_disabled'),
                    style: const TextStyle(color: Colors.redAccent, fontSize: 20, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    status['killMessage'] ?? L10n.t('contact_developer'),
                    style: const TextStyle(color: Colors.white70, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  ElevatedButton(
                    onPressed: () => exit(0),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Text(
                      L10n.t('exit_app'),
                      style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
      return;
    }

    // Check for deep link
    final deepLink = DeepLinkService.instance.consumeInitialDeepLink();

    Navigator.of(context).pushReplacement(
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) =>
            const MainScreen(),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(opacity: animation, child: child);
        },
        transitionDuration: const Duration(milliseconds: 800),
      ),
    );

    // If there's a deep link, navigate to movie detail after MainScreen is built
    if (deepLink != null) {
      Future.delayed(const Duration(milliseconds: 500), () {
        if (deepLink.action == 'movie' && deepLink.slug.isNotEmpty) {
          DeepLinkService.navigatorKey.currentState?.push(
            MaterialPageRoute(
              builder: (_) => MovieDetailScreen(slug: deepLink.slug),
            ),
          );
        } else if (deepLink.action == 'local_file' &&
            deepLink.slug.isNotEmpty) {
          final file = File(deepLink.slug);
          if (file.existsSync()) {
            final filename = deepLink.slug.split(r'\').last.split('/').last;
            final fileUrl = 'file:///' + deepLink.slug.replaceAll(r'\', '/');
            DeepLinkService.navigatorKey.currentState?.push(
              MaterialPageRoute(
                builder: (_) => PlayerScreen(
                  episodes: [
                    Episode(
                      name: 'Full',
                      slug: 'full',
                      m3u8Url: fileUrl,
                      embedUrl: '',
                    ),
                  ],
                  currentEpisodeIndex: 0,
                  movieName: filename,
                ),
              ),
            );
          }
        }
      });
    }
  }

  @override
  void dispose() {
    _player.dispose();
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Content
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ScaleTransition(
                  scale: _scaleAnimation,
                  child: Container(
                    decoration: BoxDecoration(
                      boxShadow: [
                        BoxShadow(
                          color: Colors.blueAccent.withOpacity(0.5),
                          blurRadius: _glowAnimation.value,
                          spreadRadius: _glowAnimation.value / 2,
                        ),
                      ],
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Image.asset(
                      'assets/logo.png',
                      width: 150,
                      height: 150,
                    ),
                  ),
                ),
                const SizedBox(height: 24),
                const CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.blueAccent),
                ),
              ],
            ),
          ),

          // Title Bar
          const Positioned(top: 0, left: 0, right: 0, child: CustomTitleBar()),
        ],
      ),
    );
  }
}
