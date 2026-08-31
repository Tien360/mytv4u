with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Make the banner full screen
c = c.replace("height: currentBannerHeight,", "bottom: 0, // Make banner full screen")

# 2. Add the safe GradientBlurBackground helper class
blur_class = """
class GradientBlurBackground extends StatelessWidget {
  final double startY;
  final double endY;
  final double maxBlur;

  const GradientBlurBackground({
    super.key,
    required this.startY,
    required this.endY,
    this.maxBlur = 15.0,
  });

  @override
  Widget build(BuildContext context) {
    final int steps = 5;
    final double stepHeight = (endY - startY) / steps;
    
    List<Widget> layers = [];
    
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
if "class GradientBlurBackground" not in c:
    c += "\n" + blur_class


# 3. Add the Gradient Blur Layer to the Stack
# We will inject it RIGHT AFTER the Banner (Background Media)
banner_end = c.find("// 2. Full-screen touch overlay")
if banner_end != -1:
    new_layer = """
          // 1.5 Safe Gradient Blur Layer
          Positioned.fill(
            child: LayoutBuilder(
              builder: (context, constraints) {
                return GradientBlurBackground(
                  startY: constraints.maxHeight * 0.15,
                  endY: constraints.maxHeight * 0.4,
                  maxBlur: 15.0,
                );
              }
            ),
          ),
          
          // 2. Full-screen touch overlay"""
    c = c.replace("// 2. Full-screen touch overlay", new_layer)


# 4. Remove the hard black gradient from the CustomScrollView!
# In the original UI, the CustomScrollView has a Container with a black gradient.
old_container = """                      SliverToBoxAdapter(
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Colors.black.withOpacity(0.0),
                                Colors.black.withOpacity(0.8),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.15, 1.0],
                            ),
                          ),
                          child: Padding("""

new_container = """                      SliverToBoxAdapter(
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Colors.black.withOpacity(0.0),
                                Colors.black.withOpacity(0.5),
                                Colors.black.withOpacity(0.9),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.05, 0.2, 1.0],
                            ),
                          ),
                          child: Padding("""
c = c.replace(old_container, new_container)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Applied safe full-screen UI without controllers")
