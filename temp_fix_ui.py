import sys

with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add CustomTitleBar import
if "import '../widgets/custom_title_bar.dart';" not in c:
    c = c.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\nimport '../widgets/custom_title_bar.dart';")

# 2. Fix the banner display
target_banner = """          if (_gameInfo != null && _gameInfo!.thumbUrl.isNotEmpty)
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              height: 400,
              child: ShaderMask(
                shaderCallback: (rect) {
                  return const LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Colors.black, Colors.transparent],
                  ).createShader(Rect.fromLTRB(0, 0, rect.width, rect.height));
                },
                blendMode: BlendMode.dstIn,
                child: Image.network(
                  _gameInfo!.thumbUrl,
                  fit: BoxFit.cover,
                  color: Colors.black.withOpacity(0.5),
                  colorBlendMode: BlendMode.darken,
                ),
              ),
            ),"""

new_banner = """          if (_gameInfo != null && _gameInfo!.thumbUrl.isNotEmpty)
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: ShaderMask(
                shaderCallback: (rect) {
                  return const LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Colors.black, Colors.transparent],
                  ).createShader(Rect.fromLTRB(0, 0, rect.width, rect.height));
                },
                blendMode: BlendMode.dstIn,
                child: Image.network(
                  _gameInfo!.thumbUrl,
                  fit: BoxFit.fitWidth,
                  color: Colors.black.withOpacity(0.5),
                  colorBlendMode: BlendMode.darken,
                ),
              ),
            ),"""

if target_banner in c:
    c = c.replace(target_banner, new_banner)
    print("Fixed banner display")
else:
    print("Could not find target_banner")

# 3. Add CustomTitleBar to Stack
title_bar = """
          // Window Controls
          const Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: CustomTitleBar(),
          ),
"""

# Insert CustomTitleBar before SafeArea
if "child: CustomTitleBar()" not in c:
    c = c.replace("          // Main Content\n          SafeArea(", title_bar + "\n          // Main Content\n          SafeArea(")
    print("Added CustomTitleBar")

with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)

