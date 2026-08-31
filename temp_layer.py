import sys

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# --- PART 1: Fix Ambient Background ---
ambient_start = c.find("// 0. Ambient Blurred Background")
ambient_end = c.find("// 1. Background Media")

if ambient_start != -1 and ambient_end != -1:
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
          
          // 0.1 The Gradient Blurred Image (For the bottom content when at top)
          Positioned.fill(
            child: ShaderMask(
              shaderCallback: (Rect bounds) {
                return const LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Colors.transparent, Colors.white],
                  stops: [0.15, 0.4], // Starts blurring at 15% height, fully blurred at 40%
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

          // 0.2 The Full-Screen Blur (Fades in when scrolling down)
          Positioned.fill(
            child: AnimatedBuilder(
              animation: _scrollController,
              builder: (context, child) {
                double opacity = 0.0;
                if (_scrollController.hasClients) {
                  opacity = (_scrollController.offset / 300).clamp(0.0, 1.0);
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

          // 0.3 The Dark Gradient overlay for text readability
          Positioned.fill(
            child: AnimatedBuilder(
              animation: _scrollController,
              builder: (context, child) {
                double scrollOpacity = 0.0;
                if (_scrollController.hasClients) {
                   scrollOpacity = (_scrollController.offset / 400).clamp(0.0, 1.0);
                }
                return Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.black.withValues(alpha: 0.1 + (0.5 * scrollOpacity)), // Darkens top when scrolled
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

# --- PART 2: Strip out the old Stack/BackdropFilter from CustomScrollView ---
# We need to find the `SliverToBoxAdapter` for Content
content_start = c.find("                      // Ph n Content")
if content_start == -1:
    content_start = c.find("                      // Phần Content")

if content_start != -1:
    # Find the Padding start
    padding_idx = c.find("child: Padding(", content_start)
    if padding_idx != -1:
        # Get the balanced Padding string
        def get_balanced(text, start):
            count = 0
            for i in range(start, len(text)):
                if text[i] == '(': count += 1
                elif text[i] == ')':
                    count -= 1
                    if count == 0: return i
            return -1

        padding_end = get_balanced(c, padding_idx + len("child: "))
        padding_str = c[padding_idx + len("child: "):padding_end+1]
        
        # Where does the SliverToBoxAdapter end?
        # Let's find `],` which is the end of slivers array
        slivers_end = c.find("                    ],", content_start)
        
        new_content = """                      // Phần Content đè lên dưới của Video
                      SliverToBoxAdapter(
                        child: """ + padding_str + """
                      ),
"""
        c = c[:content_start] + new_content + c[slivers_end:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Architecture replaced!")
