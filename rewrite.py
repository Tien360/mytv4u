import sys

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Rename classes
c = c.replace("class MovieDetailScreen extends", "class MovieDetailScreenTest extends")
c = c.replace("class _MovieDetailScreenState extends State<MovieDetailScreen>", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest>")
c = c.replace("State<MovieDetailScreen> createState() => _MovieDetailScreenState();", "State<MovieDetailScreenTest> createState() => _MovieDetailScreenTestState();")
c = c.replace("=> MovieDetailScreen(", "=> MovieDetailScreenTest(")

# 2. Add Test indicator to title
c = c.replace("title: _movie!.name,", "title: '${_movie!.name} (\U0001f9ea Bản Test)',")

# 3. Add scroll controller for main content
c = c.replace("class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {", "class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> {\n  final ScrollController _mainScrollController = ScrollController();\n")
# find the first dispose to add it
c = c.replace("super.dispose();", "_mainScrollController.dispose();\n    super.dispose();", 1)

# 4. Replace Ambient Background (Lines 1630-1660 roughly)
# We find exactly the block to replace.
ambient_start = c.find("// 0. Ambient Blurred Background")
ambient_end = c.find("// 1. Background Media")

new_ambient = """          // 0. The Base Clear Image
          Positioned.fill(
            child: Hero(
              tag: widget.heroTag ?? widget.slug,
              child: CachedNetworkImage(
                imageUrl: heroImage,
                fit: BoxFit.cover,
                alignment: Alignment.topCenter,
              ),
            ),
          ),
          
          // 0.1 The Gradient Blurred Image
          Positioned.fill(
            child: ShaderMask(
              shaderCallback: (Rect bounds) {
                return const LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Colors.transparent, Colors.white],
                  stops: [0.15, 0.4],
                ).createShader(bounds);
              },
              blendMode: BlendMode.dstIn,
              child: ImageFiltered(
                imageFilter: ImageFilter.blur(sigmaX: 25.0, sigmaY: 25.0),
                child: CachedNetworkImage(
                  imageUrl: heroImage,
                  fit: BoxFit.cover,
                  alignment: Alignment.topCenter,
                ),
              ),
            ),
          ),

          // 0.2 The Full-Screen Blur
          Positioned.fill(
            child: AnimatedBuilder(
              animation: _mainScrollController,
              builder: (context, child) {
                double opacity = 0.0;
                if (_mainScrollController.hasClients) {
                  opacity = (_mainScrollController.offset / 300).clamp(0.0, 1.0);
                }
                if (opacity == 0) return const SizedBox.shrink();
                return Opacity(
                  opacity: opacity,
                  child: ImageFiltered(
                    imageFilter: ImageFilter.blur(sigmaX: 25.0, sigmaY: 25.0),
                    child: CachedNetworkImage(
                      imageUrl: heroImage,
                      fit: BoxFit.cover,
                      alignment: Alignment.topCenter,
                    ),
                  ),
                );
              },
            ),
          ),

          // 0.3 The Dark Gradient
          Positioned.fill(
            child: AnimatedBuilder(
              animation: _mainScrollController,
              builder: (context, child) {
                double scrollOpacity = 0.0;
                if (_mainScrollController.hasClients) {
                   scrollOpacity = (_mainScrollController.offset / 400).clamp(0.0, 1.0);
                }
                return Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.black.withValues(alpha: 0.1 + (0.5 * scrollOpacity)),
                        Colors.black.withValues(alpha: 0.75),
                        Colors.black.withValues(alpha: 0.95),
                      ],
                      stops: const [0.0, 0.4, 1.0],
                    ),
                  ),
                );
              },
            ),
          ),

"""
c = c[:ambient_start] + new_ambient + c[ambient_end:]

# 5. Fix Banner (Remove background image, keep only webview)
banner_start = c.find("// 1. Background Media")
stack_start = c.find("child: Stack(", banner_start)
# We know the inner `Positioned.fill` has `Webview` and `Hero`
old_banner_content = """                Positioned.fill(
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
                ),"""
new_banner_content = """                Positioned.fill(
                  child: _showInlineTrailer && _isWebviewInitialized
                      ? Webview(_webviewController)
                      : const SizedBox.shrink(),
                ),"""
c = c.replace(old_banner_content, new_banner_content)


# 6. Remove the old content container gradient and BackdropFilter!
# Find the exact code snippet for CustomScrollView content
content_start = c.find("child: CustomScrollView(")
c = c.replace("child: CustomScrollView(", "controller: _mainScrollController,\n                  child: CustomScrollView(")

# Then we find the SliverToBoxAdapter that has the black gradient
# It starts with:
old_container = """                      // Phần Content đè lên dưới của Video
                      SliverToBoxAdapter(
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
# We just replace this opening part with Padding!
new_container = """                      // Phần Content đè lên dưới của Video
                      SliverToBoxAdapter(
                        child: Padding("""
if old_container not in c:
    # try ascii version
    old_container2 = """                      // Ph n Content `A" lAn d>i c a Video
                      SliverToBoxAdapter(
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
    if old_container2 in c:
        old_container = old_container2
    else:
        # try regex to match it loosely
        import re
        c = re.sub(r"// Ph.*?Content.*?\n\s*SliverToBoxAdapter\(\s*child:\s*Container\(\s*decoration:\s*BoxDecoration\(\s*gradient:\s*LinearGradient\([^)]+\)\s*,\s*\)\s*,\s*child:\s*Padding\(", r"// Phần Content\n                      SliverToBoxAdapter(\n                        child: Padding(", c, flags=re.DOTALL)

if old_container in c:
    c = c.replace(old_container, new_container)

# Now remove the closing brackets of that Container!
# The padding ends right before `const SizedBox(height: 100)`
# Actually, the container wraps the column.
# Let's use regex to replace the exact end of the SliverToBoxAdapter for content.
import re
c = re.sub(r"const SizedBox\(height: 100\),.*?\]\s*,\s*\)\s*,\s*\)\s*,\s*\)\s*,\s*\]\s*,\s*\)\s*,", r"const SizedBox(height: 100),\n                            ],\n                          ),\n                        ),\n                      ),\n                    ],\n                  ),\n", c, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Done")
