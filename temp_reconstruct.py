with open("build_method.txt", "r", encoding="utf-16") as f:
    build_code = f.read()

# Replace the title to have " (🧪 Bản Test)"
build_code = build_code.replace("title: _movie!.name", "title: '${_movie!.name} (🧪 Bản Test)'")

# Replace "0. Ambient Blurred Background"
ambient_start = build_code.find("// 0. Ambient Blurred Background")
ambient_end = build_code.find("// 1. Background Media")

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
build_code = build_code[:ambient_start] + new_ambient + build_code[ambient_end:]


# Fix Banner: Remove CachedNetworkImage from banner stack
banner_start = build_code.find("// 1. Background Media")
stack_start = build_code.find("child: Stack(", banner_start)
stack_end = build_code.find("              ),", stack_start)

# We know the Stack originally has Webview and Hero.
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
build_code = build_code.replace(old_banner_content, new_banner_content)


# Remove SliverToBoxAdapter's Background
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
                        child: Padding("""
build_code = build_code.replace(old_container, new_container)


import re
build_code = re.sub(r"const SizedBox\(height: 100\),.*?\n\s*\],\n\s*\),\n\s*\),\n\s*\),", r"const SizedBox(height: 100),\n                            ],\n                          ),\n                      ),", build_code, flags=re.DOTALL)


with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    full_code = f.read()

b_start = full_code.find("  @override\n  Widget build(BuildContext context) {")
if b_start != -1:
    b_end = full_code.find("\n  Widget _buildBadgeIcon(", b_start)
    if b_end != -1:
        full_code = full_code[:b_start] + build_code + full_code[b_end:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(full_code)

print("Reconstructed successfully!")
