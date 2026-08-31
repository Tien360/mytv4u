import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class FastFuriousEasterEgg {
  static bool _isPlaying = false;
  static final Random _random = Random();

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(4) + 1; // 1 to 4
    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _FastFuriousWidget(
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

class _FastFuriousWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _FastFuriousWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_FastFuriousWidget> createState() => _FastFuriousWidgetState();
}

class _FastFuriousWidgetState extends State<_FastFuriousWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    try {
      String soundFile = 'vroom.mp3';
      
      switch (widget.effectType) {
        case 1: soundFile = 'family.mp3'; break;
        case 2: soundFile = 'car_rev.mp3'; break;
        case 3: soundFile = 'vroom.mp3'; break;
        case 4: soundFile = 'vroom.mp3'; break;
      }
      
      await _player.open(Media('asset://assets/easter/sfx/$soundFile'), play: true);
    } catch (e) {
      print("Error playing easter sound: $e");
    }

    int durationMs = 3500; 
    await Future.delayed(Duration(milliseconds: durationMs));
    
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

    return IgnorePointer(
      child: Material(
        color: Colors.transparent,
        child: Stack(
          children: [
            if (widget.effectType == 1) _buildFamily(size),
            if (widget.effectType == 2) _buildKhoi(size),
            if (widget.effectType == 3) _buildOhYeah(size),
            if (widget.effectType == 4) _buildRideDie(size),
          ],
        ),
      ),
    );
  }

  // 1. Family - Zoom in at center and shake
  Widget _buildFamily(Size size) {
    return Center(
      child: Image.asset(
        "assets/easter/Fast and Furious/i don't have friend i got family.gif",
        width: size.width * 0.8,
        fit: BoxFit.contain,
      )
      .animate()
      .scale(begin: const Offset(0.5, 0.5), end: const Offset(1, 1), duration: 500.ms, curve: Curves.easeOutBack)
      .shake(hz: 3, duration: 2500.ms)
      .fadeOut(delay: 2500.ms, duration: 500.ms),
    );
  }

  // 2. Khói bốc lên - Grow from bottom
  Widget _buildKhoi(Size size) {
    return Positioned(
      bottom: 0,
      left: 0,
      right: 0,
      child: Image.asset(
        'assets/easter/Fast and Furious/khói bóc lên.gif',
        height: size.height * 0.6,
        fit: BoxFit.cover,
      )
      .animate()
      .fadeIn(duration: 500.ms)
      .scale(begin: const Offset(1, 0.5), end: const Offset(1, 1.2), duration: 2500.ms, alignment: Alignment.bottomCenter)
      .fadeOut(delay: 2500.ms, duration: 500.ms),
    );
  }

  // 3. Oh Yeah - Slide from top
  Widget _buildOhYeah(Size size) {
    return Positioned(
      top: -300,
      left: size.width / 2 - 200,
      child: Image.asset(
        'assets/easter/Fast and Furious/oh yeah.gif',
        width: 400,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: size.height / 2 + 100, duration: 800.ms, curve: Curves.easeOutBack)
      .then(delay: 1500.ms)
      .moveY(begin: 0, end: size.height + 300, duration: 600.ms, curve: Curves.easeIn),
    );
  }

  // 4. Ride or Die - Dash across screen
  Widget _buildRideDie(Size size) {
    return Positioned(
      bottom: size.height / 4,
      left: -500,
      child: Image.asset(
        'assets/easter/Fast and Furious/ride or die.gif',
        width: 400,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: size.width + 800, duration: 2000.ms, curve: Curves.easeInOutSine),
    );
  }
}
