import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Update the heroLogos type
content = content.replace("Map<String, String> _heroLogos = {};", "Map<String, TmdbLogoInfo> _heroLogos = {};")

# Inject the logo fetch inside _loadHeroMovies, specifically where backdrop is fetched
backdrop_fetch = """            final backdrop = await PhimApi.getMovieTmdbBackdrop(
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
content = content.replace(backdrop_fetch, backdrop_replace)

logo_assign = """                if (backdrop != null && backdrop.isNotEmpty) {
                  m.posterUrl = backdrop;
                }"""

logo_assign_replace = """                if (backdrop != null && backdrop.isNotEmpty) {
                  m.posterUrl = backdrop;
                }
                if (logoInfo != null) {
                  _heroLogos[m.slug] = logoInfo;
                }"""
content = content.replace(logo_assign, logo_assign_replace)

# Now, replace the builder to render it correctly
start_marker = "// Title / Logo"
end_marker = "const SizedBox(height: 12),"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_block = """// Title / Logo
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
                                      ),
                                      """
    content = content[:idx_start] + new_block + content[idx_end:]


# Timer from 8 to 15 seconds
content = re.sub(
    r"Timer\.periodic\(const Duration\(seconds: 8\),",
    r"Timer.periodic(const Duration(seconds: 15),",
    content
)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
