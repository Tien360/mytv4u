import os
content = '''
import 'package:flutter/material.dart';
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
    _setupAnimations();
  }

  void _setupAnimations() {
    int count = widget.type == 'waves' ? 15 : 7;
    _controllers = List.generate(count, (index) {
      return AnimationController(
        vsync: this,
        duration: Duration(milliseconds: 250 + math.Random().nextInt(300)),
      );
    });
    _animations = _controllers.map((controller) {
      return Tween<double>(begin: 8.0, end: widget.type == 'waves' ? 30.0 : 40.0).animate(
        CurvedAnimation(parent: controller, curve: Curves.easeInOutSine)
      );
    }).toList();
    
    _startOrStop();
  }

  @override
  void didUpdateWidget(AudioVisualizer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.type != widget.type) {
      for (var c in _controllers) {
        c.dispose();
      }
      _setupAnimations();
    } else if (oldWidget.isPlaying != widget.isPlaying) {
      _startOrStop();
    }
  }

  void _startOrStop() {
    if (widget.isPlaying) {
      for (int i = 0; i < _controllers.length; i++) {
        Future.delayed(Duration(milliseconds: i * (widget.type == 'waves' ? 30 : 0)), () {
          if (mounted && widget.isPlaying) _controllers[i].repeat(reverse: true);
        });
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
    bool isWave = widget.type == 'waves';
    int count = isWave ? 15 : 7;
    
    return SizedBox(
      height: 40,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: List.generate(count, (index) {
          return AnimatedBuilder(
            animation: _controllers[index],
            builder: (context, child) {
              return Container(
                margin: EdgeInsets.symmetric(horizontal: isWave ? 2 : 4),
                width: isWave ? 4 : 8,
                height: _animations[index].value,
                decoration: BoxDecoration(
                  color: isWave ? Colors.blueAccent.withOpacity(0.8) : Colors.white,
                  borderRadius: BorderRadius.circular(4),
                  boxShadow: [
                    BoxShadow(color: (isWave ? Colors.blueAccent : Colors.white).withOpacity(0.5), blurRadius: 4, offset: const Offset(0, 2))
                  ]
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
open('lib/screens/audio_visualizer.dart', 'w', encoding='utf-8').write(content)
