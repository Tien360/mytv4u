import re

# 1. Update TonearmWidget to be top-right pivot and inward swing
tonearm_code = '''import 'package:flutter/material.dart';
import 'dart:math' as math;

class TonearmWidget extends StatelessWidget {
  final bool isPlaying;

  const TonearmWidget({super.key, required this.isPlaying});

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween<double>(
        begin: 0.0, // Resting outside (straight down)
        end: isPlaying ? 25.0 : 0.0 // Clockwise = leftwards (inward)
      ),
      duration: const Duration(milliseconds: 1000),
      curve: Curves.easeInOut,
      builder: (context, angle, child) {
        return Transform(
          alignment: const Alignment(0, -0.8), // Pivot at top center of widget
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
    // Head angled inward (left)
    canvas.rotate(15 * math.pi / 180);
    canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(-8, 0, 16, 35), const Radius.circular(2)), darkPaint);
    
    // Stylus
    canvas.drawCircle(const Offset(0, 25), 2, Paint()..color=Colors.redAccent);
    
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
'''
open('lib/widgets/tonearm_widget.dart', 'w', encoding='utf-8').write(tonearm_code)

# 2. Update audio_player_screen.dart (Tonearm Position and Music Icon Fallback)
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Change Tonearm position
content = content.replace('top: -10,\n                                        left: 10,\n                                        child: TonearmWidget', 'top: -10,\n                                        right: 10,\n                                        child: TonearmWidget')

# Change Music Icon fallback for Podcast
old_podcast = '''                                  child: coverArt == null
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        )
                                      : null,'''
new_podcast = '''                                  child: coverArt == null
                                      ? const Padding(
                                          padding: EdgeInsets.all(48.0),
                                          child: Icon(Icons.mic, size: 80, color: Colors.blueAccent),
                                        )
                                      : null,'''
content = content.replace(old_podcast, new_podcast)

# Change Music Icon fallback for Vinyl
old_vinyl_bg = '''                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),'''
new_vinyl_bg = '''                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : null,'''
content = content.replace(old_vinyl_bg, new_vinyl_bg)

old_vinyl_hole = '''                                            if (coverArt != null)
                                              Container(
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black.withOpacity(0.2),
                                                ),
                                              ),
                                            // Center hole'''
new_vinyl_hole = '''                                            if (coverArt != null)
                                              Container(
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black.withOpacity(0.2),
                                                ),
                                              ),
                                            if (coverArt == null)
                                              const Icon(Icons.music_note, size: 80, color: Colors.white24),
                                            // Center hole'''
content = content.replace(old_vinyl_hole, new_vinyl_hole)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

