import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_logic = """                                            if (_tmdbLogoInfo != null) {
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
                                                  if (_tmdbLogoInfo!.lang == L10n.currentLang) {
                                                    showMainTitle = false;
                                                  } else if (_tmdbLogoInfo!.lang == 'none') {
                                                    showMainTitle = true;
                                                  } else {
                                                    showMainTitle = true;
                                                    showSubTitle = false;
                                                  }
                                                }"""

new_logic = """                                            if (_tmdbLogoInfo != null) {
                                                if (L10n.currentLang == 'en') {
                                                  mainTitle = _tmdbLogoInfo!.tmdbEnName.isNotEmpty ? _tmdbLogoInfo!.tmdbEnName : mainTitle;
                                                  subTitle = _tmdbLogoInfo!.tmdbOriginalName.isNotEmpty ? _tmdbLogoInfo!.tmdbOriginalName : subTitle;
                                                } else {
                                                  subTitle = _tmdbLogoInfo!.tmdbEnName.isNotEmpty ? _tmdbLogoInfo!.tmdbEnName : subTitle;
                                                }
                                              } else {
                                                if (L10n.currentLang == 'en' && _movie!.originalName.isNotEmpty) {
                                                  mainTitle = _movie!.originalName;
                                                }
                                              }
  
                                              bool showMainTitle = true;
                                              if (_tmdbLogoInfo?.url != null) {
                                                if (_tmdbLogoInfo!.lang == 'vi') {
                                                  showMainTitle = false;
                                                }
                                              }
                                              bool showSubTitle = subTitle.isNotEmpty && subTitle != mainTitle;"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced showMainTitle logic!")
else:
    print("Old logic not found!")
