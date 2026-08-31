import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class TomJerryEasterEgg {
  static bool _isPlaying = false;
  static final Random _random = Random();

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(7) + 1; // 1 to 7
    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _TomJerryWidget(
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

class _TomJerryWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _TomJerryWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_TomJerryWidget> createState() => _TomJerryWidgetState();
}

class _TomJerryWidgetState extends State<_TomJerryWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    try {
      String soundFile = 'swoosh.wav'; // Default 
      
      switch (widget.effectType) {
        case 1: soundFile = 'punch.mp3'; break; // Angry Jerry
        case 2: soundFile = 'swoosh.wav'; break; // Jerry run
        case 3: soundFile = 'gong.mp3'; break; // Hello
        case 4: soundFile = 'swoosh.wav'; break; // Tom run
        case 5: soundFile = 'swoosh.wav'; break; // Don't care
        case 6: soundFile = 'swoosh.wav'; break; // Sneaking
        case 7: soundFile = 'tom_scream.mp3'; break; // Electrocuted
      }
      
      await _player.open(Media('asset://assets/easter/sfx/$soundFile'), play: true);
    } catch (e) {
      print("Error playing easter sound: $e");
    }

    int durationMs = 3500; 
    if (widget.effectType == 7) durationMs = 4500;
    
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
            if (widget.effectType == 1) _buildAngryJerry(size),
            if (widget.effectType == 2) _buildJerryRun(size),
            if (widget.effectType == 3) _buildHello(size),
            if (widget.effectType == 4) _buildTomRun(size),
            if (widget.effectType == 5) _buildDontCare(size),
            if (widget.effectType == 6) _buildSneaking(size),
            if (widget.effectType == 7) _buildElectrocuted(size),
          ],
        ),
      ),
    );
  }

  // 1. Angry Jerry - Pop up and shake
  Widget _buildAngryJerry(Size size) {
    return Positioned(
      bottom: 20,
      left: 20,
      child: Image.asset(
        'assets/easter/Tom và Jerry/Angry jerry Sticker by Tom & Jerry.gif',
        width: 250,
        fit: BoxFit.contain,
      )
      .animate()
      .scale(begin: const Offset(0.0, 0.0), end: const Offset(1, 1), duration: 500.ms, curve: Curves.easeOutBack)
      .shake(hz: 8, duration: 2500.ms)
      .fadeOut(delay: 2500.ms, duration: 500.ms),
    );
  }

  // 2. Jerry Run - Dart across screen
  Widget _buildJerryRun(Size size) {
    return Positioned(
      bottom: 50,
      left: -300,
      child: Image.asset(
        'assets/easter/Tom và Jerry/chuột jerry chạy trốn.gif',
        width: 200,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: size.width + 500, duration: 1500.ms, curve: Curves.easeInOut),
    );
  }

  // 3. Hello - Slide down from top
  Widget _buildHello(Size size) {
    return Positioned(
      top: -300,
      left: size.width / 2 - 150,
      child: Image.asset(
        'assets/easter/Tom và Jerry/How Ya Doin Hello Sticker by Tom & Jerry.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: 350, duration: 800.ms, curve: Curves.bounceOut)
      .then(delay: 2000.ms)
      .moveY(begin: 0, end: -350, duration: 800.ms, curve: Curves.easeIn),
    );
  }

  // 4. Tom Run - Chase across screen
  Widget _buildTomRun(Size size) {
    return Positioned(
      bottom: 50,
      right: -300,
      child: Image.asset(
        'assets/easter/Tom và Jerry/mèo tom chạy.gif',
        width: 250,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: -(size.width + 500), duration: 2000.ms, curve: Curves.easeInOut),
    );
  }

  // 5. Don't Care - Pop up bottom right
  Widget _buildDontCare(Size size) {
    return Positioned(
      bottom: -300,
      right: 50,
      child: Image.asset(
        "assets/easter/Tom và Jerry/mèo tom don't care.gif",
        width: 250,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: -320, duration: 800.ms, curve: Curves.easeOutBack)
      .then(delay: 2000.ms)
      .moveY(begin: 0, end: 320, duration: 800.ms, curve: Curves.easeInBack),
    );
  }

  // 6. Sneaking - Sneak slowly
  Widget _buildSneaking(Size size) {
    return Positioned(
      bottom: 20,
      left: -300,
      child: Image.asset(
        'assets/easter/Tom và Jerry/mèo tom lén lút.gif',
        width: 250,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: size.width / 2 + 150, duration: 3000.ms, curve: Curves.linear),
    );
  }

  // 7. Electrocuted - Center shake violently
  Widget _buildElectrocuted(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/Tom và Jerry/tom bị điện giật.gif',
        width: 350,
        fit: BoxFit.contain,
      )
      .animate()
      .fadeIn(duration: 200.ms)
      .shake(hz: 15, duration: 3500.ms)
      .fadeOut(delay: 3500.ms, duration: 500.ms),
    );
  }
}
