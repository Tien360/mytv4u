import re

# 1. Update TonearmWidget
content = '''import 'package:flutter/material.dart';
import 'dart:math' as math;

class TonearmWidget extends StatelessWidget {
  final bool isPlaying;

  const TonearmWidget({super.key, required this.isPlaying});

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween<double>(
        // When stopped: angle outward (-20 deg). When playing: angle inward onto record (25 deg)
        begin: -20.0, 
        end: isPlaying ? 25.0 : -20.0
      ),
      duration: const Duration(milliseconds: 1000),
      curve: Curves.easeInOut,
      builder: (context, angle, child) {
        return Transform(
          alignment: const Alignment(0, -0.8), // Pivot point slightly below the very top
          transform: Matrix4.rotationZ(angle * math.pi / 180),
          child: child,
        );
      },
      child: CustomPaint(
        size: const Size(60, 200),
        painter: TonearmPainter(),
      ),
    );
  }
}

class TonearmPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()..color = Colors.grey[400]!..style = PaintingStyle.fill;
    final Paint darkPaint = Paint()..color = Colors.grey[800]!..style = PaintingStyle.fill;
    final Paint silverPaint = Paint()..color = Colors.grey[300]!..style = PaintingStyle.fill;

    // Pivot base
    canvas.drawCircle(Offset(size.width / 2, 20), 20, darkPaint);
    canvas.drawCircle(Offset(size.width / 2, 20), 12, paint);
    canvas.drawCircle(Offset(size.width / 2, 20), 5, darkPaint);

    canvas.save();
    canvas.translate(size.width / 2, 20);
    // Arm
    final Rect armRect = Rect.fromLTWH(-4, 0, 8, 140);
    canvas.drawRect(armRect, silverPaint);
    
    // Counterweight
    canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(-12, -25, 24, 20), const Radius.circular(4)), darkPaint);

    // Headshell
    canvas.translate(0, 140);
    // Head angled inward
    canvas.rotate(-15 * math.pi / 180);
    canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(-8, 0, 16, 35), const Radius.circular(2)), darkPaint);
    
    // Stylus
    canvas.drawCircle(const Offset(0, 25), 2, Paint()..color=Colors.redAccent);
    
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
'''
open('lib/widgets/tonearm_widget.dart', 'w', encoding='utf-8').write(content)
