import 'dart:convert';
import '../utils/noise_asset.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:shared_preferences/shared_preferences.dart';

final ValueNotifier<String?> globalAmbientImageUrl = ValueNotifier<String?>(null);
final ValueNotifier<bool> globalEnableAmbient = ValueNotifier<bool>(true);

Future<void> initAmbientSettings() async {
  final prefs = await SharedPreferences.getInstance();
  globalEnableAmbient.value = prefs.getBool('enable_ambient_bg') ?? true;
}

class AmbientBackground extends StatefulWidget {
  const AmbientBackground({super.key});

  @override
  State<AmbientBackground> createState() => _AmbientBackgroundState();
}

class _AmbientBackgroundState extends State<AmbientBackground> with SingleTickerProviderStateMixin {
  late AnimationController _breathingController;

  @override
  void initState() {
    super.initState();
    _breathingController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 15),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _breathingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<bool>(
      valueListenable: globalEnableAmbient,
      builder: (context, isEnabled, child) {
        if (!isEnabled) {
          return Container(color: const Color(0xFF000000));
        }

        return ValueListenableBuilder<String?>(
          valueListenable: globalAmbientImageUrl,
          builder: (context, imageUrl, child) {
            return AnimatedSwitcher(
              duration: const Duration(milliseconds: 4000),
              child: imageUrl == null
                  ? Container(key: const ValueKey('empty'), color: const Color(0xFF0F172A))
                  : AnimatedBuilder(
                      key: ValueKey(imageUrl),
                      animation: _breathingController,
                      builder: (context, child) {
                        return Transform.scale(
                          scale: 1.05 + (_breathingController.value * 0.05),
                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              CachedNetworkImage(
                                imageUrl: imageUrl,
                                fit: BoxFit.cover,
                                errorWidget: (context, url, error) => Container(color: const Color(0xFF0F172A)),
                              ),
                              BackdropFilter(
                                filter: ImageFilter.blur(sigmaX: 150.0, sigmaY: 150.0),
                                child: Container(
                                  color: Colors.black.withOpacity(0.6), // Darken the bright colors slightly
                                ),
                              ),
                              // Noise overlay to prevent color banding
                              Opacity(
                                opacity: 0.04,
                                child: Image.memory(
                                  base64Decode(noiseBase64),
                                  repeat: ImageRepeat.repeat,
                                  fit: BoxFit.none,
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            );
          },
        );
      },
    );
  }
}
