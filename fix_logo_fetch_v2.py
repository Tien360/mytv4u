import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Let's match the backdrop fetching block and replace it
regex = r"(final backdrop = await PhimApi\.getMovieTmdbBackdrop\([\s\S]*?isTvSeries,\s*\);)\s*if \(mounted && backdrop != null && backdrop\.isNotEmpty\) \{\s*setState\(\(\) \{\s*_heroMovies\[i\] = m\.copyWith\(posterUrl: backdrop\);\s*\}\);\s*\}"

new_block = r"""\1
            
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

if re.search(regex, content):
    content = re.sub(regex, new_block, content)
    with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("REGEX FAILED TO MATCH")
