import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

pattern = r'Positioned\.fill\(\s*child: _showInlineTrailer && _isWebviewInitialized\s*\?\s*Webview\(_webviewController\)\s*:\s*\(hasBackdrop\s*\?\s*Hero\(\s*tag: widget\.heroTag \?\? widget\.slug,\s*child: CachedNetworkImage\(\s*imageUrl: heroImage,\s*fit: BoxFit\.cover,\s*alignment: Alignment\.topCenter,\s*\),\s*\)\s*:\s*const SizedBox\.shrink\(\)\),\s*\),'

new_stack = """Positioned.fill(
                  child: Stack(
                    children: [
                      // Base image
                      if (hasBackdrop)
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
                      // Webview (Always mounted once initialized so JS executes properly, hidden via Offstage)
                      if (_isWebviewInitialized)
                        Positioned.fill(
                          child: Offstage(
                            offstage: !_showInlineTrailer,
                            child: Webview(_webviewController),
                          ),
                        ),
                    ],
                  ),
                ),"""

if re.search(pattern, c):
    c = re.sub(pattern, new_stack, c, count=1)
    print("Found and replaced in original!")
else:
    print("Pattern not found in original!")

# Now fix the pause function (remove about:blank)
c = c.replace("await _webviewController.loadUrl('about:blank');", "")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
