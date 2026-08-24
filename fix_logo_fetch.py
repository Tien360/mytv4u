import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            final backdrop = await PhimApi.getMovieTmdbBackdrop(
              m.name,
              m.originalName,
              m.year,
              isTvSeries,
            );
            if (mounted && backdrop != null && backdrop.isNotEmpty) {
              setState(() {
                _heroMovies[i] = m.copyWith(posterUrl: backdrop);
              });
            }"""

new_block = """            final backdrop = await PhimApi.getMovieTmdbBackdrop(
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
                if (logoInfo != null && logoInfo.url != null) {
                  _heroLogos[m.slug] = logoInfo;
                }
              });
            }"""

content = content.replace(old_block, new_block)

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced successfully!")
