import sys, re
with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add "🧪 Giao diện Test" label to Title Bar
title_bar_pattern = r"(CustomTitleBar\([\s\S]*?)(title: \'(.*?)\',)"
title_bar_replacement = r"\1title: '\3 (🧪 Bản Test)',"
c = re.sub(title_bar_pattern, title_bar_replacement, c)

# 2. Fix the height logic
height_logic = r"final double fullHeight = MediaQuery\.of\(context\)\.size\.width \* 9 / 16;\n\s*final double collapsedHeight = fullHeight > 450\.0 \? 450\.0 : fullHeight;\n\s*final double currentBannerHeight = _isTrailerExpanded\n\s*\? fullHeight\n\s*: collapsedHeight;"
new_height_logic = """final double fullHeight = MediaQuery.of(context).size.width * 9 / 16;
    final double currentBannerHeight = MediaQuery.of(context).size.height; // Full screen background!
    final double trailerHeight = _isTrailerExpanded ? fullHeight : (fullHeight > 450.0 ? 450.0 : fullHeight);
"""
c = re.sub(height_logic, new_height_logic, c)

# 3. Separate Trailer from Background Image
# Currently: Positioned(height: currentBannerHeight, child: Stack( ... image & trailer ... ))
# We need the trailer to have `trailerHeight`, but image has `currentBannerHeight`.
# The current code:
banner_pattern = r"(// Banner Area \(Top\)[\s\S]*?Positioned\(\s*top: 0,\s*left: 0,\s*right: 0,\s*height: )currentBannerHeight,([\s\S]*?child: Stack\(\s*fit: StackFit\.expand,\s*children: \[)"
c = re.sub(banner_pattern, r"\1currentBannerHeight,\2", c)

# Inside the Stack, the trailer uses Positioned.fill. Let's find the trailer part.
# The trailer part is:
trailer_part = r"Positioned\.fill\(\s*child: _showInlineTrailer && _isWebviewInitialized[\s\S]*?\? Webview\(_webviewController\)[\s\S]*?: \(hasBackdrop"

new_trailer_part = """Positioned(
                  top: 0,
                  left: 0,
                  right: 0,
                  height: currentBannerHeight, // We let the image fill the whole height
                  child: hasBackdrop"""
c = re.sub(r"Positioned\.fill\(\s*child: _showInlineTrailer && _isWebviewInitialized[\s\S]*?: \(hasBackdrop", new_trailer_part, c)

# Now we need to re-add the trailer on top, but with `trailerHeight`
# Where did the trailer go? I replaced `_showInlineTrailer ? Webview : hasBackdrop...` with just `hasBackdrop...`
# But I must close the old parenthesis properly.
