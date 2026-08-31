import sys, re
with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update Title Bar to indicate Test
c = re.sub(r"(CustomTitleBar\([\s\S]*?)(title: \'(.*?)\',)", r"\1title: '\3 (🧪 Bản Test)',", c)

# 2. Fix ambient background to use `heroImage` and light blur
ambient_pattern = r"(// 0\. Ambient Blurred Background[\s\S]*?Positioned\.fill\(\s*child: CachedNetworkImage\(\s*imageUrl: )_movie!\.thumbUrl(,\s*fit: BoxFit\.cover,\s*\),\s*\),\s*Positioned\.fill\(\s*child: isMinimalistUi\.value\s*\?\s*Container\(color: Colors\.black87\)\s*:\s*BackdropFilter\(\s*filter: ImageFilter\.blur\()sigmaX: 80\.0, sigmaY: 80\.0(\),[\s\S]*?child: Container\(\s*color: Colors\.black\.)withOpacity\(0\.6\)"

ambient_replace = r"\1heroImage\2sigmaX: 4.0, sigmaY: 4.0\3withOpacity(0.3)"
c = re.sub(ambient_pattern, ambient_replace, c)

# 3. Modify the Banner Area: Only keep Trailer, remove the `CachedNetworkImage` of the backdrop from here
banner_pattern = r"(// 1\. Background Media \(Banner / Trailer\)[\s\S]*?height: currentBannerHeight,\s*child: Stack\(\s*children: \[\s*Positioned\.fill\(\s*child: _showInlineTrailer && _isWebviewInitialized\s*\?\s*Webview\(_webviewController\)\s*:\s*\()hasBackdrop[\s\S]*?const SizedBox\.shrink\(\)\)(\),\s*\),\s*\])"
banner_replace = r"\1const SizedBox.shrink()\2"
c = re.sub(banner_pattern, banner_replace, c)

# 4. Find the Content Container and wrap it with BackdropFilter
content_start = c.find("                      // Ph n Content")
if content_start != -1:
    content_end = c.find("                    ],", content_start) # End of slivers list
    if content_end != -1:
        # Extract the SliverToBoxAdapter block
        block = c[content_start:content_end]
        
        # Replace the opening Container with BackdropFilter
        block = block.replace("child: Container(\n                          decoration: BoxDecoration(\n                            gradient: LinearGradient(\n                              colors: [\n                                Colors.black.withOpacity(0.0),\n                                Colors.black.withOpacity(0.8),\n                                Colors.black,", 
        """child: ClipRRect(
                          child: BackdropFilter(
                            filter: ImageFilter.blur(sigmaX: 25.0, sigmaY: 25.0),
                            child: Container(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  colors: [
                                    Colors.black.withOpacity(0.0),
                                    Colors.black.withOpacity(0.6),
                                    Colors.black.withOpacity(0.85),""")
        
        # We need to add `),)` at the end of the block, right before the last `)` of SliverToBoxAdapter
        # The block ends with:
        #                       ),
        #                     ),
        # Wait, the block text ends exactly where "                    ]," is found.
        # Let's see the end of `block`.
        # Typical end:
        #                           ],
        #                         ),
        #                       ),
        #                     ),
        
        # Let's just find the last `)` and prepend `),)`
        last_paren_idx = block.rfind(")")
        block = block[:last_paren_idx] + "),\n                          ),\n                        )" + block[last_paren_idx+1:]
        
        c = c[:content_start] + block + c[content_end:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Regex replaced")
