import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _heroLogos declaration
content = content.replace("Map<String, String> _heroLogos = {};", "Map<String, TmdbLogoInfo> _heroLogos = {};")

# 2. Update _loadHeroMovies to fetch TmdbLogoInfo instead of String
fetch_logo_old = """
          // Load logo cho hero movies
          for (var movie in _heroMovies) {
            final logoInfo = await PhimApi.getTmdbLogo(movie.name, movie.originalName);
            if (logoInfo != null && logoInfo.logoUrl != null && mounted) {
              setState(() {
                _heroLogos[movie.slug] = logoInfo.logoUrl!;
              });
            }
          }
"""

fetch_logo_new = """
          // Load logo cho hero movies
          for (var movie in _heroMovies) {
            final logoInfo = await PhimApi.getTmdbLogo(movie.name, movie.originalName);
            if (logoInfo != null && logoInfo.logoUrl != null && mounted) {
              setState(() {
                _heroLogos[movie.slug] = logoInfo;
              });
            }
          }
"""
content = content.replace(fetch_logo_old, fetch_logo_new)
# In case it was written differently:
content = re.sub(r"_heroLogos\[movie\.slug\]\s*=\s*logoInfo\.logoUrl!;", r"_heroLogos[movie.slug] = logoInfo;", content)

# 3. Update the logo rendering in Builder
builder_old = """                                        // Title / Logo
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
                                        else"""

builder_new = """                                        // Title / Logo
                                        Builder(
                                            builder: (context) {
                                              final currentHero = _heroMovies[_currentHeroIndex];
                                              final logoInfo = _heroLogos[currentHero.slug];
                                              String mainTitle = currentHero.name;
                                              String subTitle = currentHero.originalName;
                                              
                                              if (logoInfo != null && logoInfo.logoUrl != null) {
                                                final bool isDarkLogo = logoInfo.brightness != null && logoInfo.brightness! < 128;
                                                return Container(
                                                  constraints: const BoxConstraints(
                                                    maxHeight: 120,
                                                    maxWidth: 400,
                                                  ),
                                                  alignment: Alignment.centerLeft,
                                                  child: Stack(
                                                    alignment: Alignment.centerLeft,
                                                    children: [
                                                      if (isDarkLogo)
                                                        Positioned.fill(
                                                          child: ImageFiltered(
                                                            imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
                                                            child: Image.network(
                                                              logoInfo.logoUrl!,
                                                              fit: BoxFit.contain,
                                                              alignment: Alignment.centerLeft,
                                                              color: Colors.white.withOpacity(0.5),
                                                            ),
                                                          ),
                                                        ),
                                                      Image.network(
                                                        logoInfo.logoUrl!,
                                                        fit: BoxFit.contain,
                                                        alignment: Alignment.centerLeft,
                                                        errorBuilder: (context, error, stackTrace) {
                                                          return Text(
                                                            currentHero.displayName,
                                                            style: const TextStyle(
                                                              color: Colors.white,
                                                              fontSize: 40,
                                                              fontWeight: FontWeight.bold,
                                                              height: 1.1,
                                                            ),
                                                          );
                                                        },
                                                      ),
                                                    ],
                                                  ),
                                                );
                                              } else {
                                                return Column(
                                                  crossAxisAlignment: CrossAxisAlignment.start,
                                                  children: [
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
                                                    if (subTitle.isNotEmpty && subTitle != mainTitle) ...[
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
                                                    ]
                                                  ],
                                                );
                                              }
                                            },
                                        ),
"""

# Using re to properly match the Builder section
content = content.replace(builder_old, builder_new)

# 4. Timer from 8 to 15 seconds
content = content.replace("Timer.periodic(const Duration(seconds: 8),", "Timer.periodic(const Duration(seconds: 15),")


with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
