import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("final tmdbId = _tmdbDetails != null ? _tmdbDetails!['id']?.toString() : null;", "final tmdbId = _tmdbDetails != null ? int.tryParse(_tmdbDetails!['id']?.toString() ?? '') : null;")
c = c.replace("await TmdbApi.getTvDetails(tmdbId);", "await TmdbApi.getTvDetails(tmdbId, L10n.currentLang);")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed type error")
