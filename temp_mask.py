import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove GradientBlurBackground class
c = re.sub(r'class GradientBlurBackground extends StatelessWidget \{.*?(?=\Z)', '', c, flags=re.DOTALL)

# 2. Replace the background Stack
pattern = r'                if \(!\(_showInlineTrailer && _isWebviewInitialized\)\)\s*Positioned\.fill\(\s*child: LayoutBuilder\(\s*builder: \(context, constraints\) \{\s*return GradientBlurBackground\(\s*startY: currentBannerHeight - 100,\s*endY: currentBannerHeight \+ 100,\s*maxBlur: 15\.0,\s*\);\s*\}\s*\),\s*\),'

new_blur_layer = """                if (!(_showInlineTrailer && _isWebviewInitialized) && hasBackdrop)
                  Positioned.fill(
                    child: ShaderMask(
                      shaderCallback: (bounds) {
                        return const LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            Colors.transparent,
                            Colors.white,
                          ],
                          stops: [0.35, 0.7], // Smooth transition
                        ).createShader(bounds);
                      },
                      blendMode: BlendMode.dstIn,
                      child: ImageFiltered(
                        imageFilter: ImageFilter.blur(sigmaX: 6.0, sigmaY: 6.0), // Reduced blur as requested
                        child: CachedNetworkImage(
                          imageUrl: heroImage,
                          fit: BoxFit.cover,
                          alignment: Alignment.topCenter,
                        ),
                      ),
                    ),
                  ),"""

c = re.sub(pattern, new_blur_layer, c, count=1)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Applied ImageFiltered with ShaderMask")
