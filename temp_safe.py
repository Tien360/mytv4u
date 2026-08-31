with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Rename classes
c = c.replace("class MovieDetailScreen extends", "class MovieDetailScreenTest extends")
c = c.replace("class _MovieDetailScreenState extends State<MovieDetailScreen>", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest>")
c = c.replace("State<MovieDetailScreen> createState() => _MovieDetailScreenState();", "State<MovieDetailScreenTest> createState() => _MovieDetailScreenTestState();")
c = c.replace("=> MovieDetailScreen(", "=> MovieDetailScreenTest(")
c = c.replace("const MovieDetailScreen({", "const MovieDetailScreenTest({")
c = c.replace("title: _movie!.name,", "title: '${_movie!.name} (\U0001f9ea Bản Test)',")

# 2. Extract the safe stepped blur background code
blur_code = """
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
    c += "\n" + blur_code

if "import 'dart:ui';" not in c:
    c = "import 'dart:ui';\n" + c

# 3. Replace the background in the build method
# In the original, the background is an AnimatedPositioned inside the Stack.
# We will replace it with our safe, full-screen background WITHOUT Hero.

start_target = """            AnimatedPositioned(
              duration: const Duration(milliseconds: 400),
              curve: Curves.easeInOut,
              top: 0,
              left: 0,
              right: 0,
              height: currentBannerHeight,
              child: Stack(
                children: [
                  Positioned.fill(
                    child: _showInlineTrailer && _isWebviewInitialized
                        ? Webview(_webviewController)
                        : (hasBackdrop
                              ? Hero(
                                  tag: widget.heroTag ?? widget.slug,
                                  child: CachedNetworkImage(
                                    imageUrl: heroImage,
                                    fit: BoxFit.cover,
                                    alignment: Alignment.topCenter,
                                  ),
                                )
                              : const SizedBox.shrink()),
                  ),
                  // Gradient over image
                  Positioned.fill(
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.bottomCenter,
                          end: Alignment.topCenter,
                          colors: [
                            Colors.black,
                            Colors.black.withOpacity(0.0),
                          ],
                          stops: const [0.0, 0.4],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),"""

# We want the background to be full screen (bottom: 0), no Hero, and use the GradientBlurBackground.
# AND we still want the inline trailer to work if active.
new_target = """            Positioned.fill(
              child: Stack(
                children: [
                  // 1. Base Image (No Hero to avoid transition crashes on Windows)
                  Positioned.fill(
                    child: _showInlineTrailer && _isWebviewInitialized
                        ? Webview(_webviewController)
                        : (hasBackdrop
                              ? CachedNetworkImage(
                                  imageUrl: heroImage,
                                  fit: BoxFit.cover,
                                  alignment: Alignment.topCenter,
                                )
                              : const SizedBox.shrink()),
                  ),
                  
                  // 2. Safe Stepped Gradient Blur (only when no trailer)
                  if (!(_showInlineTrailer && _isWebviewInitialized))
                    Positioned.fill(
                      child: LayoutBuilder(
                        builder: (context, constraints) {
                          // start blur at banner bottom area
                          return GradientBlurBackground(
                            startY: currentBannerHeight - 100,
                            endY: currentBannerHeight + 100,
                            maxBlur: 15.0,
                          );
                        }
                      ),
                    ),
                ],
              ),
            ),"""

c = c.replace(start_target, new_target)

# 4. Remove the hard black gradient in the CustomScrollView SliverToBoxAdapter container
# Find the exact gradient code in CustomScrollView
gradient_target = """                      SliverToBoxAdapter(
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
                          ),"""

new_gradient = """                      SliverToBoxAdapter(
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Colors.black.withOpacity(0.0),
                                Colors.black.withOpacity(0.4),
                                Colors.black.withOpacity(0.85),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.05, 0.15, 1.0], // Fade to black much faster to cover text, while still letting blur show
                            ),
                          ),"""

c = c.replace(gradient_target, new_gradient)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Safely updated background layer in test screen")
