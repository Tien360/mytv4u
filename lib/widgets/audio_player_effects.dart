import 'dart:math';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'audio_visualizer.dart';

class AudioPlayerEffects extends StatefulWidget {
  final Player player;
  final VideoController controller;
  final bool isPlaying;
  final bool hasAlbumArt;
  final Duration duration;

  const AudioPlayerEffects({
    Key? key,
    required this.player,
    required this.controller,
    required this.isPlaying,
    required this.hasAlbumArt,
    required this.duration,
  }) : super(key: key);

  @override
  State<AudioPlayerEffects> createState() => _AudioPlayerEffectsState();
}

class _AudioPlayerEffectsState extends State<AudioPlayerEffects>
    with SingleTickerProviderStateMixin {
  late AnimationController _spinController;

  @override
  void initState() {
    super.initState();
    _spinController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 5), // 12 RPM
    );
    if (widget.isPlaying) {
      _spinController.repeat();
    }
  }

  @override
  void didUpdateWidget(covariant AudioPlayerEffects oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isPlaying != oldWidget.isPlaying) {
      if (widget.isPlaying) {
        _spinController.repeat();
      } else {
        _spinController.stop();
      }
    }
  }

  @override
  void dispose() {
    _spinController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    IconData fallbackIcon = Icons.music_note;
    Color fallbackColor = Colors.blue[800]!;
    
    if (widget.duration.inMinutes >= 15) {
      fallbackIcon = Icons.mic;
      fallbackColor = Colors.deepPurple[800]!;
    }

    return SizedBox.expand(
      child: Stack(
        alignment: Alignment.center,
        children: [
          // 1. Audio Visualizer in the background - Raised up
          Positioned(
            bottom: 120, // Raised to avoid overlapping with progress bar
            left: 0,
            right: 0,
            child: Opacity(
              opacity: 0.3,
              child: AudioVisualizer(
                isPlaying: widget.isPlaying,
                color: Colors.blueAccent,
                barCount: 60,
              ),
            ),
          ),
          
          // 2. Spinning Vinyl Record
          Center(
            child: RotationTransition(
              turns: _spinController,
              child: Container(
                width: 320,
                height: 320,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      Color(0xFF2A2A2A),
                      Color(0xFF111111),
                    ],
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.8),
                      blurRadius: 30,
                      spreadRadius: 10,
                    )
                  ],
                ),
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    // Grooves texture
                    Container(
                      margin: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white24, width: 0.5),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.all(35),
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white24, width: 0.5),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.all(60),
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white24, width: 0.5),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.all(80),
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white12, width: 0.5),
                      ),
                    ),

                    // Center Image (Album art OR default label)
                    ClipOval(
                      child: SizedBox(
                        width: 150,
                        height: 150,
                        child: widget.hasAlbumArt
                            ? Transform.scale(
                                scale: 1.2,
                                child: Video(
                                  controller: widget.controller,
                                  controls: NoVideoControls,
                                ),
                              )
                            : Container(
                                color: fallbackColor,
                                child: Center(
                                  child: Icon(
                                    fallbackIcon,
                                    size: 60,
                                    color: Colors.white70,
                                  ),
                                ),
                              ),
                      ),
                    ),

                    // Center hole
                    Container(
                      width: 16,
                      height: 16,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.black,
                        border: Border.all(color: Colors.white38, width: 1),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
