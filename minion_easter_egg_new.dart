import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MinionEasterEgg {
  static bool _isPlaying = false;
  static final Random _random = Random();

  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(12) + 1; 
    final overlayState = Overlay.of(context);
    late OverlayEntry overlayEntry;

    overlayEntry = OverlayEntry(
      builder: (context) => _MinionEggWidget(
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

class _MinionEggWidget extends StatefulWidget {
  final int effectType;
  final VoidCallback onComplete;

  const _MinionEggWidget({
    required this.effectType,
    required this.onComplete,
  });

  @override
  State<_MinionEggWidget> createState() => _MinionEggWidgetState();
}

class _MinionEggWidgetState extends State<_MinionEggWidget> {
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

    int durationMs = 4500; 

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
            if (widget.effectType == 1) _buildLauManHinh(size),
            if (widget.effectType == 2) _buildHunManHinh(size),
            if (widget.effectType == 3) _buildCaDamXumChao(size),
            if (widget.effectType == 4) _buildBiCaNuot(size),
            if (widget.effectType == 5) _buildTraiTim(size),
            if (widget.effectType == 6) _buildBiBat(size),
            if (widget.effectType == 7) _buildBiCan(size),
            if (widget.effectType == 8) _buildKemNhay(size),
            if (widget.effectType == 9) _buildMetMoi(size),
            if (widget.effectType == 10) _buildNhayMua(size),
            if (widget.effectType == 11) _buildPhatDien(size),
            if (widget.effectType == 12) _buildThachDau(size),
          ],
        ),
      ),
    );
  }

  Widget _buildLauManHinh(Size size) {
    return Stack(
      children: [
        // Bụi mờ dơ màn hình
        Container(
          color: Colors.brown.withOpacity(0.4),
        )
        .animate()
        .fadeOut(delay: 1500.ms, duration: 2500.ms), // Từ từ sạch khi lau
        
        Center(
          child: Image.asset(
            'assets/easter/minions/lau màn hình.gif',
            width: size.width * 1.5,
            height: size.height * 1.5,
            fit: BoxFit.cover,
          )
          .animate()
          .fadeIn(duration: 500.ms)
          .scale(begin: const Offset(1.2, 1.2), end: const Offset(1.0, 1.0), duration: 4000.ms)
          .fadeOut(delay: 4000.ms, duration: 500.ms),
        ),
      ],
    );
  }

  Widget _buildHunManHinh(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/minions/hun màn hình.gif',
        width: 400,
        fit: BoxFit.contain,
      )
      .animate()
      .scale(begin: const Offset(0.5, 0.5), end: const Offset(2.5, 2.5), duration: 2500.ms, curve: Curves.easeInCirc)
      .fadeOut(delay: 3000.ms, duration: 500.ms),
    );
  }

  Widget _buildCaDamXumChao(Size size) {
    return Positioned(
      bottom: -400,
      left: size.width / 2 - 250,
      child: Image.asset(
        'assets/easter/minions/cả đám xúm chào.gif',
        width: 500,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: -400, duration: 800.ms, curve: Curves.easeOutBack)
      .then(delay: 2000.ms)
      .moveY(begin: 0, end: 400, duration: 800.ms, curve: Curves.easeInBack),
    );
  }

  Widget _buildBiCaNuot(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/minions/bị cá nuốt cả đám.gif',
        width: size.width * 0.8,
        fit: BoxFit.contain,
      )
      .animate()
      .fadeIn(duration: 500.ms)
      .shake(hz: 4, duration: 2000.ms)
      .fadeOut(delay: 3500.ms, duration: 500.ms),
    );
  }

  Widget _buildTraiTim(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/minions/tụ đám thành trái tim.gif',
        width: 500,
        fit: BoxFit.contain,
      )
      .animate()
      .scale(begin: const Offset(0, 0), end: const Offset(1, 1), duration: 800.ms, curve: Curves.elasticOut)
      .fadeOut(delay: 3500.ms, duration: 500.ms),
    );
  }

  Widget _buildBiBat(Size size) {
    return Positioned(
      top: -300,
      left: size.width / 2 - 150,
      child: Image.asset(
        'assets/easter/minions/bị bắt.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: 350, duration: 1000.ms, curve: Curves.bounceOut)
      .then(delay: 1500.ms)
      .moveY(begin: 0, end: -350, duration: 800.ms, curve: Curves.easeIn),
    );
  }

  Widget _buildBiCan(Size size) {
    return Positioned(
      bottom: 50,
      left: -400,
      child: Image.asset(
        'assets/easter/minions/bị cắn.gif',
        width: 350,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: size.width + 500, duration: 4000.ms, curve: Curves.linear),
    );
  }

  Widget _buildKemNhay(Size size) {
    return Positioned(
      bottom: -200,
      left: 100,
      child: Image.asset(
        'assets/easter/minions/kem nhảy.gif',
        width: 250,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: -250, duration: 500.ms, curve: Curves.easeOutQuad)
      .then(delay: 2500.ms)
      .moveY(begin: 0, end: 250, duration: 500.ms, curve: Curves.easeInQuad),
    );
  }

  Widget _buildMetMoi(Size size) {
    return Positioned(
      bottom: -250,
      right: 100,
      child: Image.asset(
        'assets/easter/minions/mệt mỏi.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveY(begin: 0, end: -250, duration: 2000.ms, curve: Curves.easeOut)
      .then(delay: 1000.ms)
      .moveY(begin: 0, end: 250, duration: 1500.ms, curve: Curves.easeIn),
    );
  }

  Widget _buildNhayMua(Size size) {
    return Positioned(
      bottom: 0,
      left: size.width / 2 - 200,
      child: Image.asset(
        'assets/easter/minions/nhảy múa.gif',
        width: 400,
        fit: BoxFit.contain,
      )
      .animate()
      .fadeIn(duration: 300.ms)
      .scale(begin: const Offset(0.5, 0.5), end: const Offset(1, 1), duration: 500.ms, curve: Curves.easeOutBack)
      .fadeOut(delay: 3500.ms, duration: 500.ms),
    );
  }

  Widget _buildPhatDien(Size size) {
    return Center(
      child: Image.asset(
        'assets/easter/minions/phát điên.gif',
        width: 450,
        fit: BoxFit.contain,
      )
      .animate()
      .scale(begin: const Offset(0.2, 0.2), end: const Offset(1.2, 1.2), duration: 300.ms, curve: Curves.easeOut)
      .shake(hz: 10, duration: 3000.ms)
      .fadeOut(delay: 3000.ms, duration: 500.ms),
    );
  }

  Widget _buildThachDau(Size size) {
    return Positioned(
      bottom: 20,
      left: -300,
      child: Image.asset(
        'assets/easter/minions/thách đấu.gif',
        width: 300,
        fit: BoxFit.contain,
      )
      .animate()
      .moveX(begin: 0, end: 400, duration: 600.ms, curve: Curves.easeOutBack)
      .then(delay: 2000.ms)
      .moveX(begin: 0, end: -400, duration: 600.ms, curve: Curves.easeInBack),
    );
  }
}
