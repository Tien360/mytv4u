import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_logic = """                                              if (_tmdbLogoInfo != null) {
                                                if (L10n.currentLang == 'en') {
                                                  mainTitle = _tmdbLogoInfo!.tmdbEnName;
                                                  if (mainTitle.isEmpty) mainTitle = _movie!.name;
                                                  subTitle = _tmdbLogoInfo!.tmdbOriginalName;
                                                } else {
                                                  subTitle = _tmdbLogoInfo!.tmdbEnName;
                                                }
                                              } else {
                                                if (L10n.currentLang == 'en' && _movie!.originalName.isNotEmpty) {
                                                  mainTitle = _movie!.originalName;
                                                }
                                              }
                                              if (mainTitle.isEmpty) mainTitle = "Unknown Title";

                                              bool showMainTitle = true;
                                              if (_tmdbLogoInfo?.url != null) {
                                                  if (_tmdbLogoInfo!.lang == 'vi') {
                                                    showMainTitle = false;
                                                  }
                                              }
                                              bool showSubTitle = subTitle.isNotEmpty && subTitle != mainTitle && _tmdbLogoInfo?.lang != 'en';
"""

text = re.sub(r'if \(_tmdbLogoInfo \!= null\) \{.*?showSubTitle = false;\n\s*\}\n\s*\}', new_logic, text, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Regex replace title logic!")
