import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class NarutoEasterEgg {
  static bool _isPlaying = false;
  static final Random _random = Random();

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(13) + 1; // 1 to 13
    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _NarutoWidget(
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

class _NarutoWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _NarutoWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_NarutoWidget> createState() => _NarutoWidgetState();
}

class _NarutoWidgetState extends State<_NarutoWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    try {
      String soundFile = 'swoosh.wav'; 
      
      switch (widget.effectType) {
        case 1: soundFile = 'gong.mp3'; break; // akatsuki jutsu
        case 2: soundFile = 'swoosh.wav'; break; // kakashi cute
        case 3: soundFile = 'swoosh.wav'; break; // naruto run
        case 4: soundFile = 'thwip.wav'; break; // hand signs
        case 5: soundFile = 'tom_scream.mp3'; break; // falling
        case 6: soundFile = 'heartbeat.wav'; break; // ramen
        case 7: soundFile = 'swoosh.wav'; break; // walk
        case 8: soundFile = 'gong.mp3'; break; // akatsuki group
        case 9: soundFile = 'skadoosh.mp3'; break; // rasengan
        case 10: soundFile = 'heartbeat.wav'; break; // sexy jutsu
        case 11: soundFile = 'thwip.wav'; break; // sharingan
        case 12: soundFile = 'swoosh.wav'; break; // disappear
        case 13: soundFile = 'punch.mp3'; break; // shadow clone
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
            if (widget.effectType == 1) _buildCenterScale(size, 'bọn aksuki triển khai chú.gif'),
            if (widget.effectType == 2) _buildSlideUp(size, 'kakashi đáng yêu.gif'),
            if (widget.effectType == 3) _buildDashLeft(size, 'kiểu chạy naruto.gif'),
            if (widget.effectType == 4) _buildCenterScale(size, 'kí ấn của naruto.gif'),
            if (widget.effectType == 5) _buildFallDown(size, 'naruto la té xuống.gif'),
            if (widget.effectType == 6) _buildCenterScale(size, 'naruto đang húp ramen.gif'),
            if (widget.effectType == 7) _buildSneakRight(size, 'naruto đi bộ.gif'),
            if (widget.effectType == 8) _buildSlideUp(size, 'nhóm akasuki.gif'),
            if (widget.effectType == 9) _buildRasengan(size, 'ringsegan.gif'),
            if (widget.effectType == 10) _buildCenterScale(size, 'sexybaby.gif'),
            if (widget.effectType == 11) _buildCenterScale(size, 'sharingan mắt.gif'),
            if (widget.effectType == 12) _buildDisappear(size, 'thuật biến mất.gif'),
            if (widget.effectType == 13) _buildShadowClone(size, 'ảnh phân thân chi thuật.gif'),
          ],
        ),
      ),
    );
  }

  Widget _buildCenterScale(Size size, String filename) {
    return Center(
      child: Image.asset('assets/easter/naruto/$filename', width: 350, fit: BoxFit.contain)
      .animate()
      .scale(begin: const Offset(0.5, 0.5), end: const Offset(1, 1), duration: 500.ms, curve: Curves.easeOutBack)
      .fadeOut(delay: 2500.ms, duration: 500.ms),
    );
  }

  Widget _buildSlideUp(Size size, String filename) {
    return Positioned(
      bottom: -300,
      left: size.width / 2 - 175,
      child: Image.asset('assets/easter/naruto/$filename', width: 350, fit: BoxFit.contain)
      .animate()
      .moveY(begin: 0, end: -350, duration: 800.ms, curve: Curves.easeOutBack)
      .then(delay: 2000.ms)
      .moveY(begin: 0, end: 350, duration: 800.ms, curve: Curves.easeIn),
    );
  }

  Widget _buildDashLeft(Size size, String filename) {
    return Positioned(
      bottom: 50,
      right: -300,
      child: Image.asset('assets/easter/naruto/$filename', width: 250, fit: BoxFit.contain)
      .animate()
      .moveX(begin: 0, end: -(size.width + 500), duration: 2000.ms, curve: Curves.easeInOut),
    );
  }

  Widget _buildFallDown(Size size, String filename) {
    return Positioned(
      top: -300,
      left: size.width / 2 - 150,
      child: Image.asset('assets/easter/naruto/$filename', width: 300, fit: BoxFit.contain)
      .animate()
      .moveY(begin: 0, end: size.height + 400, duration: 2000.ms, curve: Curves.easeIn),
    );
  }

  Widget _buildSneakRight(Size size, String filename) {
    return Positioned(
      bottom: 20,
      left: -200,
      child: Image.asset('assets/easter/naruto/$filename', width: 200, fit: BoxFit.contain)
      .animate()
      .moveX(begin: 0, end: size.width + 300, duration: 3500.ms, curve: Curves.linear),
    );
  }

  Widget _buildRasengan(Size size, String filename) {
    return Center(
      child: Image.asset('assets/easter/naruto/$filename', width: 400, fit: BoxFit.contain)
      .animate()
      .fadeIn(duration: 300.ms)
      .shake(hz: 5, duration: 2500.ms)
      .fadeOut(delay: 2500.ms, duration: 500.ms),
    );
  }

  Widget _buildDisappear(Size size, String filename) {
    return Center(
      child: Image.asset('assets/easter/naruto/$filename', width: 300, fit: BoxFit.contain)
      .animate()
      .fadeIn(duration: 200.ms)
      .then(delay: 1500.ms)
      .fadeOut(duration: 300.ms)
      .scale(begin: const Offset(1,1), end: const Offset(2,2), duration: 300.ms),
    );
  }

  Widget _buildShadowClone(Size size, String filename) {
    return Stack(
      children: [
        Positioned(
          top: size.height/3, left: size.width/4,
          child: Image.asset('assets/easter/naruto/$filename', width: 200).animate().fadeIn().fadeOut(delay: 2500.ms),
        ),
        Positioned(
          top: size.height/3, right: size.width/4,
          child: Image.asset('assets/easter/naruto/$filename', width: 200).animate().fadeIn(delay: 200.ms).fadeOut(delay: 2500.ms),
        ),
        Positioned(
          bottom: size.height/4, left: size.width/2 - 100,
          child: Image.asset('assets/easter/naruto/$filename', width: 200).animate().fadeIn(delay: 400.ms).fadeOut(delay: 2500.ms),
        ),
      ],
    );
  }
}
