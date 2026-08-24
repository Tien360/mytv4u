with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re

# 1. Change _movieLogo to _tmdbLogoInfo
text = re.sub(r'String\? _movieLogo;', r'TmdbLogoInfo? _tmdbLogoInfo;', text)

# 2. Change the fetch block
fetch_old = """      final logoUrl = await PhimApi.getMovieTmdbLogo(
        movie.name,
        movie.originalName,
        movie.year,
        isTvSeries,
        lang,
      );
      if (mounted && logoUrl != null) {
        setState(() {
          _movieLogo = logoUrl;
        });
      }"""
fetch_new = """      final info = await PhimApi.getMovieTmdbLogo(
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
      }"""
text = text.replace(fetch_old, fetch_new)

# 3. Change the UI block
ui_old = """                                        if (_movieLogo != null)
                                          Container(
                                            constraints: const BoxConstraints(
                                              maxHeight: 120,
                                              maxWidth: 500,
                                            ),
                                            alignment: Alignment.centerLeft,
                                            child: Image.network(
                                              _movieLogo!,
                                              fit: BoxFit.contain,
                                              alignment: Alignment.centerLeft,
                                              errorBuilder: (context, error,
                                                  stackTrace) {
                                                return Text(
                                                  _movie!.name,
                                                  style: const TextStyle(
                                                    color: Colors.white,
                                                    fontSize: 32,
                                                    fontWeight:
                                                        FontWeight.bold,
                                                  ),
                                                );
                                              },
                                            ),
                                          )
                                        else
                                          Text(
                                            _movie!.name,
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontSize: 32,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                        const SizedBox(height: 8),
                                        Text(
                                          _movie!.originalName,
                                          style: TextStyle(
                                            color:
                                                Colors.white.withOpacity(0.7),
                                            fontSize: 16,
                                          ),
                                        ),"""
ui_new = """                                        Builder(
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
                                                    child: Image.network(
                                                      _tmdbLogoInfo!.url!,
                                                      fit: BoxFit.contain,
                                                      alignment: Alignment.centerLeft,
                                                      errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                    ),
                                                  ),
                                                if (showMainTitle)
                                                  Text(
                                                    mainTitle,
                                                    style: const TextStyle(
                                                      color: Colors.white,
                                                      fontSize: 32,
                                                      fontWeight: FontWeight.bold,
                                                      shadows: [Shadow(color: Colors.black, blurRadius: 10)],
                                                    ),
                                                  ),
                                                if (showSubTitle) ...[
                                                  if (showMainTitle) const SizedBox(height: 8),
                                                  Text(
                                                    subTitle,
                                                    style: TextStyle(
                                                      color: Colors.white.withOpacity(0.7),
                                                      fontSize: 16,
                                                      shadows: const [Shadow(color: Colors.black, blurRadius: 5)],
                                                    ),
                                                  ),
                                                ],
                                              ],
                                            );
                                          },
                                        ),"""
text = text.replace(ui_old, ui_new)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
