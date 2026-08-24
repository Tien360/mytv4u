import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import for dart:ui
if "import 'dart:ui';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'dart:ui';\nimport 'package:flutter/material.dart';")

# 2. Add import for ambient_background.dart
if "import '../widgets/ambient_background.dart';" not in content:
    content = content.replace("import '../widgets/glass_search_bar.dart';", "import '../widgets/glass_search_bar.dart';\nimport '../widgets/ambient_background.dart';")

# 3. Update _heroLogos to TmdbLogoInfo
content = content.replace("Map<String, String> _heroLogos = {};", "Map<String, TmdbLogoInfo> _heroLogos = {};")

# 4. Inject _updateAmbientBackground method
if "_updateAmbientBackground" not in content:
    method = """  void _updateAmbientBackground() {
    if (_heroMovies.isNotEmpty) {
      globalAmbientImageUrl.value = _heroMovies[_currentHeroIndex].posterUrl.isNotEmpty 
          ? _heroMovies[_currentHeroIndex].posterUrl 
          : _heroMovies[_currentHeroIndex].thumbUrl;
    }
  }

  void _startHeroTimer() {"""
    content = content.replace("  void _startHeroTimer() {", method)

# 5. Add update ambient calls where _currentHeroIndex is changed
content = re.sub(
    r"_currentHeroIndex = \(_currentHeroIndex \+ 1\) % _heroMovies\.length;\s*\}\);",
    r"_currentHeroIndex = (_currentHeroIndex + 1) % _heroMovies.length;\n            _updateAmbientBackground();\n          });",
    content
)

content = re.sub(
    r"_currentHeroIndex =\n\s*\(_currentHeroIndex - 1 \+ _heroMovies\.length\) %\n\s*_heroMovies\.length;\s*\}\);",
    r"_currentHeroIndex =\n                    (_currentHeroIndex - 1 + _heroMovies.length) %\n                    _heroMovies.length;\n                _updateAmbientBackground();\n              });",
    content
)

content = re.sub(
    r"setState\(\(\) \{\n\s*_currentHeroIndex = index;\n\s*\}\);",
    r"setState(() {\n                                          _currentHeroIndex = index;\n                                          _updateAmbientBackground();\n                                        });",
    content
)

content = re.sub(
    r"_isLoadingHero = false;\n\s*\}\);",
    r"_isLoadingHero = false;\n        _updateAmbientBackground();\n      });",
    content
)

# 6. Change timer duration
content = re.sub(
    r"Timer\.periodic\(const Duration\(seconds: 8\),",
    r"Timer.periodic(const Duration(seconds: 15),",
    content
)

# 7. Add Logo fetching in _loadHeroMovies
fetch_pattern = r"(final backdrop = await PhimApi\.getMovieTmdbBackdrop\([\s\S]*?isTvSeries,\n\s*\);)"
replace_fetch = r"""\1
            final logoInfo = await PhimApi.getMovieTmdbLogo(
              m.name,
              m.originalName,
              m.year,
              isTvSeries,
              L10n.currentLang,
            );"""
content = re.sub(fetch_pattern, replace_fetch, content)

assign_pattern = r"(m\.posterUrl = backdrop;\n\s*\})"
replace_assign = r"""\1
                if (logoInfo != null && logoInfo.url != null) {
                  _heroLogos[m.slug] = logoInfo;
                }"""
content = re.sub(assign_pattern, replace_assign, content)

# 8. Replace Logo rendering block
# Use regex to find the EXACT block starting with "// Title / Logo" and ending with "else" and then the "Text" block
render_old = re.compile(r"// Title / Logo\s*if \(_heroLogos\[_heroMovies\[_currentHeroIndex\]\s*\.slug\] !=\s*null\)\s*Container\(.*?\)\s*else\s*Text\([\s\S]*?,\s*\),", re.DOTALL)

render_new = """// Title / Logo
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

content = render_old.sub(render_new, content)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
