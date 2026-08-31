import sys
with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target_bg = """      body: Stack(
        children: [
          // Ambient Background
          AmbientBackground(),"""
new_bg = """      body: Stack(
        children: [
          // Ambient Background
          AmbientBackground(),
          
          // Horizontal Banner Backdrop
          if (_gameInfo != null && _gameInfo!.thumbUrl.isNotEmpty)
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

if target_bg in c:
    c = c.replace(target_bg, new_bg)
    with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Added banner backdrop")
else:
    print("Could not find target_bg")

