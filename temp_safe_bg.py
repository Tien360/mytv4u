with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# We need to find the `Stack` children for the background.
# In the previous script, we replaced `// 0. Ambient Blurred Background` with a chunk starting with `// 0. The Base Clear Image`
# Let's find `// 0. The Base Clear Image` and replace up to `// 1. Background Media` (if it exists) or just the whole block.
start_idx = c.find("// 0. The Base Clear Image")
if start_idx != -1:
    end_idx = c.find("// 1. Background Media")
    if end_idx == -1:
        # If I removed 1. Background Media, where does it end?
        # It ends at `// 2. Full-screen touch overlay`
        end_idx = c.find("// 2. Full-screen touch overlay")
    
    if end_idx != -1:
        new_bg = """          // 0. The Base Clear Image (Full Screen)
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
          
          // 1. Gradient Blur Layer (Safe & Fast)
          Positioned.fill(
            child: ShaderMask(
              shaderCallback: (Rect bounds) {
                return const LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Colors.transparent, Colors.white],
                  stops: [0.15, 0.4], // 15% top is clear, smoothly blurs until 40%
                ).createShader(bounds);
              },
              blendMode: BlendMode.dstIn,
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 15.0, sigmaY: 15.0),
                child: Container(
                  color: Colors.transparent,
                ),
              ),
            ),
          ),

          // 2. Dark Gradient Layer (For text readability)
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.black.withValues(alpha: 0.1),
                    Colors.black.withValues(alpha: 0.8),
                    Colors.black.withValues(alpha: 0.95),
                  ],
                  stops: const [0.0, 0.4, 1.0],
                ),
              ),
            ),
          ),

"""
        c = c[:start_idx] + new_bg + c[end_idx:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Replaced background with safe BackdropFilter")
