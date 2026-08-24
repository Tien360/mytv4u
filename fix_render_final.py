import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_render = re.compile(r"// Title / Logo\s*if \(_heroLogos\[_heroMovies\[_currentHeroIndex\]\s*\.slug\] !=\s*null\)\s*Container\([\s\S]*?else\s*Text\([\s\S]*?,\s*\),\s*const SizedBox\(height: 8\),\s*// Original Name\s*Text\([\s\S]*?,\s*\),", re.DOTALL)

new_render = """// Title / Logo
                                        Builder(
                                          builder: (context) {
                                            final currentHero = _heroMovies[_currentHeroIndex];
                                            final logoInfo = _heroLogos[currentHero.slug];
                                            String mainTitle = currentHero.name;
                                            String subTitle = currentHero.originalName;
                                            
                                            if (logoInfo != null) {
                                              if (L10n.currentLang == 'en') {
                                                mainTitle = logoInfo.tmdbEnName;
                                                subTitle = logoInfo.tmdbOriginalName;
                                              } else {
                                                subTitle = logoInfo.tmdbEnName;
                                              }
                                            } else {
                                              if (L10n.currentLang == 'en') {
                                                mainTitle = currentHero.originalName;
                                              }
                                            }
                                            
                                            bool showMainTitle = true;
                                            bool showSubTitle = subTitle.isNotEmpty && subTitle != mainTitle;
                                            
                                            if (logoInfo?.url != null) {
                                              if (logoInfo!.lang == 'none') {
                                                showMainTitle = true;
                                              } else {
                                                showMainTitle = false;
                                                if (L10n.currentLang == 'vi' && logoInfo.lang == 'en') {
                                                  showMainTitle = true;
                                                  showSubTitle = false;
                                                }
                                              }
                                            }

                                            return Column(
                                              crossAxisAlignment: CrossAxisAlignment.start,
                                              children: [
                                                if (logoInfo?.url != null)
                                                  Container(
                                                    constraints: const BoxConstraints(maxHeight: 120, maxWidth: 400),
                                                    alignment: Alignment.centerLeft,
                                                    margin: EdgeInsets.only(bottom: showMainTitle ? 12 : 8),
                                                    child: Stack(
                                                      alignment: Alignment.centerLeft,
                                                      children: [
                                                        ImageFiltered(
                                                          imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
                                                          child: Image.network(
                                                            logoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.7),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),
                                                        Transform.translate(
                                                          offset: const Offset(2, 3),
                                                          child: Image.network(
                                                            logoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.black.withOpacity(0.8),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),
                                                        Image.network(
                                                          logoInfo!.url!,
                                                          fit: BoxFit.contain,
                                                          alignment: Alignment.centerLeft,
                                                          errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                if (showMainTitle)
                                                  Text(
                                                    mainTitle,
                                                    style: const TextStyle(
                                                      color: Colors.white,
                                                      fontSize: 40,
                                                      fontWeight: FontWeight.bold,
                                                      height: 1.1,
                                                      shadows: [Shadow(color: Colors.black87, blurRadius: 10)],
                                                    ),
                                                  ),
                                                if (showSubTitle) ...[
                                                  const SizedBox(height: 4),
                                                  Text(
                                                    subTitle,
                                                    style: const TextStyle(
                                                      color: Colors.white70,
                                                      fontSize: 20,
                                                      fontWeight: FontWeight.w500,
                                                      shadows: [Shadow(color: Colors.black87, blurRadius: 6)],
                                                    ),
                                                  ),
                                                ],
                                              ],
                                            );
                                          },
                                        ),"""

content = old_render.sub(new_render, content)
with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
