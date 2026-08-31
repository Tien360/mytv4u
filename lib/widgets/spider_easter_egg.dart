import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SpiderEasterEgg {
  static bool _isPlaying = false;
  static final Random _random = Random();

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(3) + 1; // 1, 2, or 3
    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _SpiderEggWidget(
        effectType: effectType,
        onComplete: () {
          _isPlaying = false;
          overlayEntry.remove();
        },
      ),
    );

    overlayState.insert(overlayEntry);
  }
}

class _SpiderEggWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _SpiderEggWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_SpiderEggWidget> createState() => _SpiderEggWidgetState();
}

class _SpiderEggWidgetState extends State<_SpiderEggWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    // Determine sound and duration based on effect
    String soundAsset = '';
    int durationMs = 0;

    if (widget.effectType == 1) { // Swing
      soundAsset = 'asset://assets/easter/sfx/swoosh.wav';
      durationMs = 4000;
    } else if (widget.effectType == 2) { // Web Shoot
      soundAsset = 'asset://assets/easter/sfx/thwip.wav';
      durationMs = 3000;
    } else if (widget.effectType == 3) { // Blood Logo
      soundAsset = 'asset://assets/easter/sfx/heartbeat.wav';
      durationMs = 4000;
    }

    try {
      await _player.open(Media(soundAsset), play: true);
    } catch (e) {
      print("Error playing easter sound: $e");
    }

    // Wait for the animation to complete
    await Future.delayed(Duration(milliseconds: durationMs));
    
    if (mounted) {
      setState(() {
        _isVisible = false;
      });
      // Small delay for fade out
      await Future.delayed(const Duration(milliseconds: 500));
      _player.dispose();
      widget.onComplete();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_isVisible) return const SizedBox.shrink();

    final size = MediaQuery.of(context).size;

    return IgnorePointer(
      child: Material(
        color: Colors.transparent,
        child: Stack(
          children: [
            if (widget.effectType == 1) _buildSwingEffect(size),
            if (widget.effectType == 2) _buildWebShootEffect(size),
            if (widget.effectType == 3) _buildBloodLogoEffect(size),
          ],
        ),
      ),
    );
  }

  Widget _buildSwingEffect(Size size) {
    return Positioned(
      top: -size.height * 0.1,
      left: size.width / 2 - 150,
      child: Image.asset(
        'assets/easter/spiderman/spider_swing.png',
        width: 300,
        height: 500,
        fit: BoxFit.contain,
      )
      .animate()
      .slideY(begin: -1.5, end: 0.1, duration: 800.ms, curve: Curves.easeOutBack)
      .then(delay: 1500.ms)
      .slideY(begin: 0.1, end: -1.5, duration: 800.ms, curve: Curves.easeInBack),
    );
  }

  Widget _buildWebShootEffect(Size size) {
    return Stack(
      children: [
        Positioned(
          top: -50,
          left: -50,
          child: Image.asset(
            'assets/easter/spiderman/spider_web.png',
            width: size.width * 0.6,
            fit: BoxFit.contain,
          )
          .animate()
          .scale(begin: const Offset(0.2, 0.2), end: const Offset(1.0, 1.0), duration: 300.ms, curve: Curves.elasticOut)
          .fadeIn(duration: 200.ms)
          .then(delay: 2000.ms)
          .fadeOut(duration: 500.ms),
        ),
        Positioned(
          bottom: -50,
          right: -50,
          child: Transform.rotate(
            angle: pi,
            child: Image.asset(
              'assets/easter/spiderman/spider_web.png',
              width: size.width * 0.6,
              fit: BoxFit.contain,
            ),
          )
          .animate(delay: 100.ms)
          .scale(begin: const Offset(0.2, 0.2), end: const Offset(1.0, 1.0), duration: 300.ms, curve: Curves.elasticOut)
          .fadeIn(duration: 200.ms)
          .then(delay: 1900.ms)
          .fadeOut(duration: 500.ms),
        ),
      ],
    );
  }

  Widget _buildBloodLogoEffect(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/spiderman/spider_logo.png',
        width: size.width * 0.5,
        fit: BoxFit.contain,
        color: Colors.redAccent.withOpacity(0.8), // Add slight eerie glow tint
        colorBlendMode: BlendMode.srcATop,
      )
      .animate()
      .fadeIn(duration: 1000.ms)
      .scale(begin: const Offset(0.8, 0.8), end: const Offset(1.0, 1.0), duration: 1000.ms, curve: Curves.easeInOut)
      .then()
      .scale(begin: const Offset(1.0, 1.0), end: const Offset(1.1, 1.1), duration: 400.ms, curve: Curves.easeInOut)
      .then()
      .scale(begin: const Offset(1.1, 1.1), end: const Offset(1.0, 1.0), duration: 400.ms, curve: Curves.easeInOut)
      .then(delay: 500.ms)
      .fadeOut(duration: 1000.ms),
    );
  }
}
