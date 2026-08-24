# -*- coding: utf-8 -*-
import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update _movieLogo to _tmdbLogoInfo
content = content.replace('String? _movieLogo;', 'TmdbLogoInfo? _tmdbLogoInfo;')

# 2. Update _fetchTmdbLogo
content = re.sub(
    r"Future<void> _fetchTmdbLogo\(Movie movie\) async \{.*?print\('Error fetching tmdb logo: \$e'\);\s*\}\s*\}",
    '''  Future<void> _fetchTmdbLogo(Movie movie) async {
    try {
      final isTvSeries =
          movie.episodes.isNotEmpty && movie.episodes.first.items.length > 1;
      final info = await PhimApi.getMovieTmdbLogo(
        movie.name,
        movie.originalName,
        movie.year,
        isTvSeries,
        L10n.currentLang,
      );
      if (mounted && info != null) {
        setState(() {
          _tmdbLogoInfo = info;
        });
      }
    } catch (e) {
      print('Error fetching tmdb logo: $e');
    }
  }''',
    content,
    flags=re.DOTALL
)

# 3. Update the logo/title rendering part exactly.
title_block_new = '''                                        Builder(
                                          builder: (context) {
                                            String mainTitle = _movie!.name;
                                            String subTitle = _movie!.originalName;

                                            if (_tmdbLogoInfo != null) {
                                              if (L10n.currentLang == 'en') {
                                                mainTitle = _tmdbLogoInfo!.tmdbEnName;
                                                subTitle = _tmdbLogoInfo!.tmdbOriginalName;
                                              } else {
                                                subTitle = _tmdbLogoInfo!.tmdbEnName;
                                              }
                                            } else {
                                              if (L10n.currentLang == 'en') {
                                                mainTitle = _movie!.originalName;
                                              }
                                            }

                                            bool showMainTitle = true;
                                            bool showSubTitle = subTitle.isNotEmpty && subTitle != mainTitle;

                                            if (_tmdbLogoInfo?.url != null) {
                                              if (_tmdbLogoInfo!.lang == 'none') {
                                                showMainTitle = true;
                                              } else {
                                                showMainTitle = false;
                                                if (L10n.currentLang == 'vi' && _tmdbLogoInfo!.lang == 'en') {
                                                  showMainTitle = true;
                                                  showSubTitle = false;
                                                }
                                              }
                                            }

                                            return Column(
                                              crossAxisAlignment: CrossAxisAlignment.start,
                                              children: [
                                                if (_tmdbLogoInfo?.url != null)
                                                  Container(
                                                    constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
                                                    alignment: Alignment.centerLeft,
                                                    margin: EdgeInsets.only(bottom: showMainTitle ? 12 : 8),
                                                    child: Stack(
                                                      alignment: Alignment.centerLeft,
                                                      children: [
                                                        Transform.translate(
                                                          offset: const Offset(1, 1),
                                                          child: Image.network(
                                                            _tmdbLogoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.5),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),
                                                        Transform.translate(
                                                          offset: const Offset(2, 3),
                                                          child: Image.network(
                                                            _tmdbLogoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.black.withOpacity(0.8),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),
                                                        Image.network(
                                                          _tmdbLogoInfo!.url!,
                                                          fit: BoxFit.contain,
                                                          alignment: Alignment.centerLeft,
                                                          errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                if (showMainTitle)
                                                  SelectableText(
                                                    mainTitle,
                                                    style: const TextStyle(
                                                      fontSize: 48,
                                                      fontWeight: FontWeight.bold,
                                                      color: Colors.white,
                                                      height: 1.1,
                                                      shadows: [
                                                        Shadow(
                                                          color: Colors.black,
                                                          blurRadius: 10,
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                if (showSubTitle) ...[
                                                  if (showMainTitle) const SizedBox(height: 8),
                                                  SelectableText(
                                                    subTitle,
                                                    style: TextStyle(
                                                      fontSize: 20,
                                                      color: Colors.white.withOpacity(0.7),
                                                      shadows: const [
                                                        Shadow(
                                                          color: Colors.black,
                                                          blurRadius: 5,
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                ]
                                              ],
                                            );
                                          },
                                        ),'''

pattern_detail = r'if \(_movieLogo != null\).*?blurRadius: 5,\s*\),\s*\]\s*,\s*\)\s*,\s*\)'
content = re.sub(pattern_detail, title_block_new, content, flags=re.DOTALL, count=1)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

# HOME SCREEN
with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    content2 = f.read()

content2 = content2.replace('Map<String, String> _heroLogos = {};', 'Map<String, TmdbLogoInfo> _heroLogos = {};')

content2 = re.sub(
    r'final isTvSeries =.*?_heroMovies\[i\] = m\.copyWith\(posterUrl: backdrop\);\s*\}\s*\)\;\s*\}',
    '''final isTvSeries =
                m.episodes.isNotEmpty && m.episodes.first.items.length > 1;
            final backdrop = await PhimApi.getMovieTmdbBackdrop(
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
            );
            if (mounted) {
              setState(() {
                if (backdrop != null && backdrop.isNotEmpty) {
                  _heroMovies[i] = m.copyWith(posterUrl: backdrop);
                }
                if (logoInfo != null) {
                  _heroLogos[m.slug] = logoInfo;
                }
              });
            }''',
    content2,
    flags=re.DOTALL
)

hero_title_new = '''Builder(
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
                                                    constraints: const BoxConstraints(
                                                      maxHeight: 120,
                                                      maxWidth: 400,
                                                    ),
                                                    alignment: Alignment.centerLeft,
                                                    margin: EdgeInsets.only(bottom: showMainTitle ? 12 : 8),
                                                    child: Stack(
                                                      alignment: Alignment.centerLeft,
                                                      children: [
                                                        Transform.translate(
                                                          offset: const Offset(1, 1),
                                                          child: Image.network(
                                                            logoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.5),
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
                                                      shadows: [Shadow(color: Colors.black, blurRadius: 10)],
                                                    ),
                                                  ),
                                                if (showSubTitle) ...[
                                                  if (showMainTitle) const SizedBox(height: 8),
                                                  Text(
                                                    subTitle,
                                                    style: TextStyle(
                                                      color: Colors.white.withOpacity(0.8),
                                                      fontSize: 16,
                                                      shadows: const [Shadow(color: Colors.black, blurRadius: 5)],
                                                    ),
                                                  ),
                                                ],
                                              ],
                                            );
                                          },
                                        ),'''

pattern_home = r'if \(_heroLogos\[_heroMovies\[_currentHeroIndex\]\s*\.slug\] !=\s*null\).*?fontSize: 16,\s*\),\s*\)'
content2 = re.sub(pattern_home, hero_title_new, content2, flags=re.DOTALL, count=1)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content2)

