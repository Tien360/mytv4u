import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Replace the AnimatedPositioned with Positioned.fill and add the blur
pattern1 = r'          AnimatedPositioned\(\s*duration: const Duration\(milliseconds: 400\),\s*curve: Curves\.easeInOut,\s*top: 0,\s*left: 0,\s*right: 0,\s*height: currentBannerHeight,\s*child: Stack\(\s*children: \[\s*Positioned\.fill\(\s*child: _showInlineTrailer && _isWebviewInitialized\s*\?\s*Webview\(_webviewController\)\s*:\s*\(hasBackdrop\s*\?\s*Hero\(\s*tag: widget\.heroTag \?\? widget\.slug,\s*child: CachedNetworkImage\(\s*imageUrl: heroImage,\s*fit: BoxFit\.cover,\s*alignment: Alignment\.topCenter,\s*\),\s*\)\s*:\s*const SizedBox\.shrink\(\)\),\s*\),\s*\],\s*\),\s*\),'

new_background = """          Positioned.fill(
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
                if (!(_showInlineTrailer && _isWebviewInitialized))
                  Positioned.fill(
                    child: LayoutBuilder(
                      builder: (context, constraints) {
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

c = re.sub(pattern1, new_background, c, count=1)

# 2. Modify the CustomScrollView gradient to let the blur show through
pattern2 = r'                            gradient: LinearGradient\(\s*colors: \[\s*Colors\.black\.withValues\(alpha: 0\.0\),\s*Colors\.black\.withValues\(alpha: 0\.8\),\s*Colors\.black,\s*\],\s*begin: Alignment\.topCenter,\s*end: Alignment\.bottomCenter,\s*stops: const \[0\.0, 0\.15, 1\.0\],\s*\),'

new_gradient = """                            gradient: LinearGradient(
                              colors: [
                                Colors.transparent,
                                Colors.black.withValues(alpha: 0.4),
                                Colors.black.withValues(alpha: 0.85),
                                Colors.black,
                              ],
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              stops: const [0.0, 0.05, 0.15, 1.0],
                            ),"""

c = re.sub(pattern2, new_gradient, c, count=1)

# 3. Add the Test badge to the title text
c = re.sub(r"Text\(\s*widget\.title,", "Text(\n                                '${widget.title} (\U0001f9ea Bản Test)',", c, count=1)


with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Python replace done.")
