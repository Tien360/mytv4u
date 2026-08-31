code = """
class GradientBlurBackground extends StatelessWidget {
  final double startY;
  final double endY;
  final double maxBlur;

  const GradientBlurBackground({
    Key? key,
    required this.startY,
    required this.endY,
    this.maxBlur = 15.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final int steps = 5;
    final double stepHeight = (endY - startY) / steps;
    
    List<Widget> layers = [];
    
    // The transitional strips
    for (int i = 0; i < steps; i++) {
      final double currentBlur = (maxBlur / steps) * (i + 1);
      layers.add(
        Positioned(
          top: startY + (i * stepHeight),
          height: stepHeight,
          left: 0,
          right: 0,
          child: ClipRect(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: currentBlur, sigmaY: currentBlur),
              child: const SizedBox.expand(),
            ),
          ),
        ),
      );
    }
    
    // The rest of the screen below endY
    layers.add(
      Positioned(
        top: endY,
        bottom: 0,
        left: 0,
        right: 0,
        child: ClipRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: maxBlur, sigmaY: maxBlur),
            child: const SizedBox.expand(),
          ),
        ),
      ),
    );

    return Stack(children: layers);
  }
}
"""

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Insert the helper class at the end of the file
if "class GradientBlurBackground" not in c:
    c += "\n" + code

# Replace the ShaderMask BackdropFilter with this new safe GradientBlurBackground
import re
# We look for `// 1. Gradient Blur Layer (Safe & Fast)` up to `// 2. Dark Gradient Layer`
start_idx = c.find("// 1. Gradient Blur Layer (Safe & Fast)")
if start_idx != -1:
    end_idx = c.find("// 2. Dark Gradient Layer")
    if end_idx != -1:
        new_layer = """          // 1. Gradient Blur Layer (Ultra-Safe Stepped Blur)
          Positioned.fill(
            child: LayoutBuilder(
              builder: (context, constraints) {
                // Starts blurring at 15% height, fully blurred at 40% height
                return GradientBlurBackground(
                  startY: constraints.maxHeight * 0.15,
                  endY: constraints.maxHeight * 0.4,
                  maxBlur: 15.0,
                );
              }
            ),
          ),

"""
        c = c[:start_idx] + new_layer + c[end_idx:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Injected GradientBlurBackground!")
