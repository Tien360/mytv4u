import os
code = '''import 'package:flutter/material.dart';
import 'dart:math' as math;

class AudioVisualizer extends StatefulWidget {
  final bool isPlaying;
  final String type;
  const AudioVisualizer({Key? key, required this.isPlaying, this.type = 'bars'}) : super(key: key);

  @override
  State<AudioVisualizer> createState() => _AudioVisualizerState();
}

class _AudioVisualizerState extends State<AudioVisualizer> with TickerProviderStateMixin {
  late List<AnimationController> _controllers;
  late List<Animation<double>> _animations;

  @override
  void initState() {
    super.initState();
    _controllers = List.generate(7, (index) {
      return AnimationController(
        vsync: this,
        duration: Duration(milliseconds: 300 + math.Random().nextInt(400)),
      );
    });
    _animations = _controllers.map((controller) {
      return Tween<double>(begin: 10.0, end: 40.0).animate(
        CurvedAnimation(parent: controller, curve: Curves.easeInOutSine)
      );
    }).toList();
    
    _startOrStop();
  }

  @override
  void didUpdateWidget(AudioVisualizer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.isPlaying != widget.isPlaying) {
      _startOrStop();
    }
  }

  void _startOrStop() {
    if (widget.isPlaying) {
      for (var c in _controllers) {
        c.repeat(reverse: true);
      }
    } else {
      for (var c in _controllers) {
        c.animateTo(0.0, duration: const Duration(milliseconds: 500));
      }
    }
  }

  @override
  void dispose() {
    for (var c in _controllers) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.type == 'waves') {
      return SizedBox(
        height: 50,
        child: AnimatedBuilder(
          animation: _controllers[0],
          builder: (context, child) {
            return Icon(
              Icons.waves,
              size: 40 + (_animations[0].value - 10) * 0.5,
              color: Colors.blueAccent,
            );
          },
        ),
      );
    }

    return SizedBox(
      height: 50,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: List.generate(7, (index) {
          return AnimatedBuilder(
            animation: _controllers[index],
            builder: (context, child) {
              return Container(
                margin: const EdgeInsets.symmetric(horizontal: 4),
                width: 8,
                height: _animations[index].value,
                decoration: BoxDecoration(
                  color: Colors.blueAccent,
                  borderRadius: BorderRadius.circular(4),
                ),
              );
            },
          );
        }),
      ),
    );
  }
}
'''
open('lib/screens/audio_visualizer.dart', 'w', encoding='utf-8').write(code)
