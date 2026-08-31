import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class KungfuPandaEasterEgg {
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
      builder: (context) => _KungfuPandaWidget(
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

class _KungfuPandaWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _KungfuPandaWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_KungfuPandaWidget> createState() => _KungfuPandaWidgetState();
}

class _KungfuPandaWidgetState extends State<_KungfuPandaWidget> {
  final Player _player = Player();
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    _playEffect();
  }

  Future<void> _playEffect() async {
    try {
      String soundFile = 'skadoosh.mp3';
      
      switch (widget.effectType) {
        case 1: soundFile = 'gong.mp3'; break; // e ngại -> gong (a bit shy/dramatic)
        case 2: soundFile = 'punch.mp3'; break; // múa võ 2
        case 3: soundFile = 'skadoosh.mp3'; break; // múa võ
        case 4: soundFile = 'hiyah.mp3'; break; // xin chào
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
            if (widget.effectType == 1) _buildENgai(size),
            if (widget.effectType == 2) _buildMuaVo2(size),
            if (widget.effectType == 3) _buildMuaVo(size),
            if (widget.effectType == 4) _buildXinChao(size),
          ],
        ),
      ),
    );
  }

  // Effect 1: E ngại (Shy) - slide in slowly from right, bob, slide back
  Widget _buildENgai(Size size) {
    return Positioned(
      bottom: 20,
      right: -300,
      child: Image.asset(
        'assets/easter/kungfu panda/e ngại.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: -350, duration: 1500.ms, curve: Curves.easeOut)
      .then(delay: 1000.ms)
      .moveX(begin: 0, end: 350, duration: 1000.ms, curve: Curves.easeIn),
    );
  }

  // Effect 2: Múa võ 2 (Martial arts 2) - dash across screen
  Widget _buildMuaVo2(Size size) {
    return Positioned(
      bottom: size.height / 3,
      left: -400,
      child: Image.asset(
        'assets/easter/kungfu panda/múa võ 2.gif',
        width: 350,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: size.width + 500, duration: 3000.ms, curve: Curves.easeInOut),
    );
  }

  // Effect 3: Múa võ (Martial arts) - pop up center bottom, do action, slide down
  Widget _buildMuaVo(Size size) {
    return Positioned(
      bottom: -300,
      left: size.width / 2 - 200,
      child: Image.asset(
        'assets/easter/kungfu panda/múa võ.gif',
        width: 400,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: -350, duration: 600.ms, curve: Curves.easeOutBack)
      .then(delay: 2000.ms)
      .moveY(begin: 0, end: 350, duration: 600.ms, curve: Curves.easeInBack),
    );
  }

  // Effect 4: Xin chào (Hello) - Drop down from top center, bow/stay, slide up
  Widget _buildXinChao(Size size) {
    return Positioned(
      top: -300,
      left: size.width / 2 - 150,
      child: Image.asset(
        'assets/easter/kungfu panda/xin chào.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: 350, duration: 1000.ms, curve: Curves.bounceOut)
      .then(delay: 1500.ms)
      .moveY(begin: 0, end: -350, duration: 800.ms, curve: Curves.easeIn),
    );
  }
}
