import 'dart:math';
import 'package:flutter/material.dart';

class AudioVisualizer extends StatefulWidget {
  final bool isPlaying;
  final Color color;
  final int barCount;
  
  const AudioVisualizer({
    super.key,
    required this.isPlaying,
    this.color = Colors.white,
    this.barCount = 30,
  });

  @override
  State<AudioVisualizer> createState() => _AudioVisualizerState();
}

class _AudioVisualizerState extends State<AudioVisualizer> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final Random _random = Random();
  late List<double> _heights;
  late List<double> _targetHeights;

  @override
  void initState() {
    super.initState();
    _heights = List.filled(widget.barCount, 0.1);
    _targetHeights = List.filled(widget.barCount, 0.1);
    
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
    )..addListener(() {
      setState(() {
        for (int i = 0; i < widget.barCount; i++) {
          _heights[i] += (_targetHeights[i] - _heights[i]) * 0.3;
        }
      });
    });
    
    _generateTargets();
    if (widget.isPlaying) {
      _controller.repeat();
    }
  }

  @override
  void didUpdateWidget(covariant AudioVisualizer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isPlaying != oldWidget.isPlaying) {
      if (widget.isPlaying) {
        _controller.repeat();
      } else {
        _controller.stop();
        setState(() {
          _targetHeights = List.filled(widget.barCount, 0.1);
        });
      }
    }
  }

  void _generateTargets() {
    if (!mounted) return;
    if (widget.isPlaying) {
      for (int i = 0; i < widget.barCount; i++) {
        // Create a bell-curve like visualizer where center bars are taller
        double distance = (i - widget.barCount / 2).abs() / (widget.barCount / 2);
        double maxH = 1.0 - (distance * 0.6); // Center is 1.0, edges are 0.4
        
        _targetHeights[i] = max(0.1, _random.nextDouble() * maxH);
      }
    }
    Future.delayed(const Duration(milliseconds: 150), _generateTargets);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FittedBox(
      fit: BoxFit.scaleDown,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
      children: List.generate(widget.barCount, (index) {
        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 2),
          width: 8,
          height: 10 + (_heights[index] * 100),
          decoration: BoxDecoration(
            color: widget.color,
            borderRadius: BorderRadius.circular(4),
            boxShadow: [
              BoxShadow(
                color: widget.color.withOpacity(0.5),
                blurRadius: 8,
                spreadRadius: 1,
              ),
            ],
          ),
        );
      }),
      ),
    );
  }
}
