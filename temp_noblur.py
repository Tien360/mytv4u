with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove the GradientBlurBackground usage
start_blur_usage = c.find("// 2. Safe Stepped Gradient Blur")
if start_blur_usage != -1:
    end_blur_usage = c.find("],", start_blur_usage)
    if end_blur_usage != -1:
        # We want to remove from start_blur_usage up to the end of the LayoutBuilder
        # Let's just use string replacement for the exact block I added in .55
        target = """                  // 2. Safe Stepped Gradient Blur (only when no trailer)
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
        c = c.replace(target, "")

# 2. To replace the blur, we will add a smooth dark gradient directly over the image, but BEFORE the CustomScrollView
# Actually, the CustomScrollView already has a container with a gradient. We can just use that!
# Let's make the CustomScrollView's gradient extremely smooth so it acts as the "mờ dần" effect.
old_gradient = """                            gradient: LinearGradient(
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

# We want the gradient to start transparent at the top, slowly fade to 90% black where the title starts, and be solid black at the bottom.
# The title starts around `SizedBox(height: screenHeight * 0.4)` or `currentBannerHeight` (450px).
# So stops around 0.0 (top), 0.4 (start fading), 0.6 (dark), 1.0 (black).
new_gradient = """                            gradient: LinearGradient(
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
c = c.replace(old_gradient, new_gradient)

# 3. Wait, I should add the Hero back to the background image if it was removed in .55?
# Yes, because the Hero animation is nice, and it wasn't the cause of the hang (BackdropFilter was).
# Let's restore the Hero tag.
old_img = """                              ? CachedNetworkImage(
                                  imageUrl: heroImage,
                                  fit: BoxFit.cover,
                                  alignment: Alignment.topCenter,
                                )"""
new_img = """                              ? Hero(
                                  tag: widget.heroTag ?? widget.slug,
                                  child: CachedNetworkImage(
                                    imageUrl: heroImage,
                                    fit: BoxFit.cover,
                                    alignment: Alignment.topCenter,
                                  ),
                                )"""
c = c.replace(old_img, new_img)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed BackdropFilter and optimized gradient")
