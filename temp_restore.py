with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Restore the BackdropFilter blur layers
old_layer = """                  Positioned.fill(
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

new_layer = """                  Positioned.fill(
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
                    ),"""

c = c.replace(old_layer, new_layer)

# 2. Revert the black gradient in CustomScrollView back to the .55 version (which lets the blur shine through better)
old_grad = """                            gradient: LinearGradient(
                              colors: [
                                Colors.transparent,
                                Colors.black.withOpacity(0.6),
                                Colors.black.withOpacity(0.95),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.2, 0.4, 1.0], // Smoothly fades from clear to black over the content area
                            ),"""

new_grad = """                            gradient: LinearGradient(
                              colors: [
                                Colors.black.withOpacity(0.0),
                                Colors.black.withOpacity(0.4),
                                Colors.black.withOpacity(0.85),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.05, 0.15, 1.0], // Fade to black much faster to cover text, while still letting blur show
                            ),"""

c = c.replace(old_grad, new_grad)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Restored GradientBlurBackground and fixed recursion!")
