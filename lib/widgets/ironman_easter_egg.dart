import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class IronmanEasterEgg {
  static bool _isPlaying = false;

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _IronmanEggWidget(
        onComplete: () {
          _isPlaying = false;
          overlayEntry.remove();
        },
      ),
    );

    overlayState.insert(overlayEntry);
  }
}

class _IronmanEggWidget extends StatefulWidget {
  final VoidCallback onComplete;

  const _IronmanEggWidget({
    required this.onComplete,
  });

  @override
  State<_IronmanEggWidget> createState() => _IronmanEggWidgetState();
}

class _IronmanEggWidgetState extends State<_IronmanEggWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    try {
      await _player.open(Media('asset://assets/easter/sfx/swoosh.wav'), play: true);
    } catch (e) {
      print("Error playing easter sound: $e");
    }

    // Wait for the animation to complete
    await Future.delayed(const Duration(milliseconds: 3000));
    
    if (mounted) {
      setState(() {
        _isVisible = false;
      });
      await Future.delayed(const Duration(milliseconds: 500));
      _player.dispose();
      widget.onComplete();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_isVisible) return const SizedBox.shrink();

    final size = MediaQuery.of(context).size;
    final random = Random();
    
    // Start from bottom left (off-screen)
    final startX = -300.0;
    final startY = size.height + 200.0;
    
    // End at top right / mid right (off-screen)
    final endX = size.width + 300.0;
    final endY = random.nextDouble() * (size.height * 0.4) - 200.0;

    return IgnorePointer(
      child: Material(
        color: Colors.transparent,
        child: Stack(
          children: [
            Positioned(
              left: 0,
              top: 0,
              child: Image.asset(
                'assets/easter/ironman/ironman_fly.png',
                width: 250,
                fit: BoxFit.contain,
              )
              .animate()
              .moveX(
                begin: startX,
                end: endX,
                duration: 2500.ms,
                curve: Curves.easeIn, 
              )
              .moveY(
                begin: startY,
                end: endY,
                duration: 2500.ms,
                curve: Curves.easeOutQuart, // Creates the arc shape
              )
              .rotate(
                begin: -0.2, // Tilted upwards initially
                end: 0.1,    // Levels out
                duration: 2500.ms,
                curve: Curves.easeInOut,
              )
              .scale(
                begin: const Offset(0.3, 0.3),
                end: const Offset(1.5, 1.5),
                duration: 2500.ms,
              )
            ),
          ],
        ),
      ),
    );
  }
}
