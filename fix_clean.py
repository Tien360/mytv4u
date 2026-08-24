import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
if "import 'dart:ui';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'dart:ui';\nimport 'package:flutter/material.dart';")

if "import '../widgets/ambient_background.dart';" not in content:
    content = content.replace("import '../widgets/glass_search_bar.dart';", "import '../widgets/ambient_background.dart';\nimport '../widgets/glass_search_bar.dart';")

# 2. _heroLogos map
content = content.replace("Map<String, String> _heroLogos = {};", "Map<String, TmdbLogoInfo> _heroLogos = {};")

# 3. _updateAmbientBackground method
if "_updateAmbientBackground" not in content:
    content = content.replace("  void _startHeroTimer() {", """  void _updateAmbientBackground() {
    if (_heroMovies.isNotEmpty) {
      globalAmbientImageUrl.value = _heroMovies[_currentHeroIndex].posterUrl.isNotEmpty 
          ? _heroMovies[_currentHeroIndex].posterUrl 
          : _heroMovies[_currentHeroIndex].thumbUrl;
    }
  }

  void _startHeroTimer() {""")

# 4. Inject _updateAmbientBackground() calls
content = content.replace(
    "_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;\n          });",
    "_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;\n            _updateAmbientBackground();\n          });"
)
content = content.replace(
    "_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;\n              });",
    "_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;\n                _updateAmbientBackground();\n              });"
)
content = content.replace(
    "setState(() {\n                                          _currentHeroIndex = index;\n                                        });",
    "setState(() {\n                                          _currentHeroIndex = index;\n                                          _updateAmbientBackground();\n                                        });"
)
content = content.replace(
    "_isLoadingHero = false;\n        });",
    "_isLoadingHero = false;\n          _updateAmbientBackground();\n        });"
)

# 5. Timer 15s
content = content.replace(
    "Timer.periodic(const Duration(seconds: 8),",
    "Timer.periodic(const Duration(seconds: 15),"
)

# 6. Fetch logos in _loadHeroMovies
backdrop_code = """            final backdrop = await PhimApi.getMovieTmdbBackdrop(
              m.name,
              m.originalName,
              m.year,
              isTvSeries,
            );"""
            
backdrop_replace = """            final backdrop = await PhimApi.getMovieTmdbBackdrop(
              m.name,
              m.originalName,
              m.year,
              isTvSeries,
            );
            
            final logoInfo = await PhimApi.getMovieTmdbLogo(
              m.name,
              m.originalName,
              m.year,
              isTvSeries,
              L10n.currentLang,
            );"""
content = content.replace(backdrop_code, backdrop_replace)

assign_code = """                if (backdrop != null && backdrop.isNotEmpty) {
                  m.posterUrl = backdrop;
                }"""
assign_replace = """                if (backdrop != null && backdrop.isNotEmpty) {
                  m.posterUrl = backdrop;
                }
                if (logoInfo != null && logoInfo.url != null) {
                  _heroLogos[m.slug] = logoInfo;
                }"""
content = content.replace(assign_code, assign_replace)

# 7. Rendering Logo
old_render = """                                        // Title / Logo
                                        if (_heroLogos[_heroMovies[_currentHeroIndex]
                                                .slug] !=
                                            null)
                                          Container(
                                            constraints: const BoxConstraints(
                                              maxHeight: 120,
                                              maxWidth: 400,
                                            ),
                                            alignment: Alignment.centerLeft,
                                            child: Image.network(
                                              _heroLogos[_heroMovies[_currentHeroIndex]
                                                  .slug]!,
                                              fit: BoxFit.contain,
                                              alignment: Alignment.centerLeft,
                                              errorBuilder:
                                                  (context, error, stackTrace) {
                                                    return Text(
                                                      _heroMovies[_currentHeroIndex]
                                                          .displayName,
                                                      style: const TextStyle(
                                                        color: Colors.white,
                                                        fontSize: 40,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                        height: 1.1,
                                                      ),
                                                    );
                                                  },
                                            ),
                                          )
                                        else
                                          Text(
                                            _heroMovies[_currentHeroIndex]
                                                .displayName,
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontSize: 40,
                                              fontWeight: FontWeight.bold,
                                              height: 1.1,
                                            ),
                                          ),
                                        const SizedBox(height: 8),
                                        // Original Name
                                        Text(
                                          _heroMovies[_currentHeroIndex]
                                              .originalName,
                                          style: TextStyle(
                                            color: Colors.white.withOpacity(0.8),
                                            fontSize: 16,
                                          ),
                                        ),"""

new_render = """                                        // Title / Logo
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

content = content.replace(old_render, new_render)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
