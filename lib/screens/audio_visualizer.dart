import 'package:flutter/material.dart';
import 'dart:math' as math;

class AudioVisualizer extends StatefulWidget {
  final bool isPlaying;
  final String type; // 'inline', 'bars', 'circle'
  final Color color;
  final double? radius; // for circle

  const AudioVisualizer({
    super.key, 
    required this.isPlaying, 
    this.type = 'inline',
    this.color = Colors.blueAccent,
    this.radius,
  });

  @override
  State<AudioVisualizer> createState() => _AudioVisualizerState();
}

class _AudioVisualizerState extends State<AudioVisualizer> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  List<double> _targetHeights = [];
  List<double> _currentHeights = [];
  final int _barsCount = 60;

  @override
  void initState() {
    super.initState();
    _currentHeights = List.filled(_barsCount, 5.0);
    _targetHeights = List.filled(_barsCount, 5.0);

    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 150));
    _controller.addListener(() {
      setState(() {
        for (int i = 0; i < _barsCount; i++) {
          _currentHeights[i] += (_targetHeights[i] - _currentHeights[i]) * 0.2;
        }
      });
    });

    _startLoop();
  }

  void _startLoop() async {
    while (mounted) {
      if (widget.isPlaying) {
        for (int i = 0; i < _barsCount; i++) {
          // Generate a smoothish random wave
          double h = 5.0 + math.Random().nextDouble() * (widget.type == 'circle' ? 40.0 : 60.0);
          _targetHeights[i] = h;
        }
      } else {
        for (int i = 0; i < _barsCount; i++) {
          _targetHeights[i] = 5.0;
        }
      }
      _controller.forward(from: 0.0);
      await Future.delayed(const Duration(milliseconds: 200));
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.type == 'circle') {
      return CustomPaint(
        size: Size.infinite,
        painter: _CircleVisualizerPainter(_currentHeights, widget.color, widget.radius ?? 160.0),
      );
    } else if (widget.type == 'bars') {
      return SizedBox(
        height: 80,
        child: CustomPaint(
          size: const Size(double.infinity, 80),
          painter: _BarsVisualizerPainter(_currentHeights, widget.color, 40),
        ),
      );
    } else {
      // inline
      return SizedBox(
        height: 24,
        width: 40,
        child: CustomPaint(
          size: const Size(40, 24),
          painter: _BarsVisualizerPainter(_currentHeights.sublist(0, 10), widget.color, 10),
        ),
      );
    }
  }
}

class _BarsVisualizerPainter extends CustomPainter {
  final List<double> heights;
  final Color color;
  final int count;

  _BarsVisualizerPainter(this.heights, this.color, this.count);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color.withOpacity(0.8)
      ..strokeCap = StrokeCap.round
      ..strokeWidth = (size.width / count) * 0.6;
      
    final glowPaint = Paint()
      ..color = color.withOpacity(0.3)
      ..strokeCap = StrokeCap.round
      ..strokeWidth = (size.width / count) * 1.5
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4.0);

    final spacing = size.width / count;
    for (int i = 0; i < count; i++) {
      double x = i * spacing + spacing / 2;
      double h = (heights[i] / 65.0) * size.height; // normalize
      h = h.clamp(4.0, size.height);
      
      canvas.drawLine(Offset(x, size.height), Offset(x, size.height - h), glowPaint);
      canvas.drawLine(Offset(x, size.height), Offset(x, size.height - h), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

class _CircleVisualizerPainter extends CustomPainter {
  final List<double> heights;
  final Color color;
  final double radius;

  _CircleVisualizerPainter(this.heights, this.color, this.radius);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color.withOpacity(0.6)
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 3.0;

    final glowPaint = Paint()
      ..color = color.withOpacity(0.3)
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 6.0
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 5.0);

    final center = Offset(size.width / 2, size.height / 2);
    final count = heights.length;
    final angleStep = (2 * math.pi) / count;

    for (int i = 0; i < count; i++) {
      double angle = i * angleStep - math.pi / 2;
      double h = heights[i];
      
      Offset start = Offset(
        center.dx + math.cos(angle) * radius,
        center.dy + math.sin(angle) * radius,
      );
      Offset end = Offset(
        center.dx + math.cos(angle) * (radius + h),
        center.dy + math.sin(angle) * (radius + h),
      );

      canvas.drawLine(start, end, glowPaint);
      canvas.drawLine(start, end, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
