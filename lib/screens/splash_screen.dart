import 'dart:async';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'main_screen.dart';
import 'movie_detail_screen.dart';
import '../widgets/custom_title_bar.dart';
import '../services/deep_link_service.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
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

    // Chuyển sang MainScreen sau 2.5s, có deep link thì mở phim luôn
    Timer(const Duration(milliseconds: 2500), () {
      if (!mounted) return;
      
      // Check for deep link
      final deepLink = DeepLinkService.instance.consumeInitialDeepLink();
      
      Navigator.of(context).pushReplacement(
        PageRouteBuilder(
          pageBuilder: (context, animation, secondaryAnimation) => const MainScreen(),
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(opacity: animation, child: child);
          },
          transitionDuration: const Duration(milliseconds: 800),
        ),
      );
      
      // If there's a deep link, navigate to movie detail after MainScreen is built
      if (deepLink != null && deepLink.action == 'movie' && deepLink.slug.isNotEmpty) {
        Future.delayed(const Duration(milliseconds: 500), () {
          DeepLinkService.navigatorKey.currentState?.push(
            MaterialPageRoute(
              builder: (_) => MovieDetailScreen(slug: deepLink.slug),
            ),
          );
        });
      }
    });
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
          const Positioned(
            top: 0, left: 0, right: 0,
            child: CustomTitleBar(),
          ),
        ],
      ),
    );
  }
}
