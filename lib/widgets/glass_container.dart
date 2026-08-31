import 'dart:ui';
import 'package:flutter/material.dart';
import '../globals.dart';

class GlassContainer extends StatelessWidget {
  final Widget child;
  final double borderRadius;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final double? width;
  final double? height;
  final Color color;
  final Color borderColor;
  final double blur;

  const GlassContainer({
    super.key,
    required this.child,
    this.borderRadius = 16.0,
    this.padding,
    this.margin,
    this.width,
    this.height,
    this.color = const Color(0x1AFFFFFF), // ~5% white
    this.borderColor = const Color(0x33FFFFFF), // ~10% white
    this.blur = 30.0,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<bool>(
      valueListenable: isMinimalistUi,
      builder: (context, isMinimalist, _) {
        final innerContainer = Container(
          padding: padding,
          decoration: BoxDecoration(
            color: isMinimalist ? const Color(0xFF1E1E1E) : color,
            borderRadius: BorderRadius.circular(borderRadius),
            border: Border.all(
              color: isMinimalist ? Colors.white12 : borderColor, 
              width: 1
            ),
          ),
          child: child,
        );

        return Container(
          margin: margin,
          width: width,
          height: height,
          child: isMinimalist
              ? innerContainer
              : ClipRRect(
                  borderRadius: BorderRadius.circular(borderRadius),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
                    child: innerContainer,
                  ),
                ),
        );
      },
    );
  }
}
