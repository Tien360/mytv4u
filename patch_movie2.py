with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
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

text = re.sub(r'if \(_movieLogo != null\).*?fontSize: 16,\s*\),\s*\),', ui_new, text, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
