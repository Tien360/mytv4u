import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

new_fetch = """  Future<List<dynamic>> _fetchAirSchedule() async {
    try {
      final tmdbId = _tmdbDetails != null ? int.tryParse(_tmdbDetails!['id']?.toString() ?? '') : null;
      if (tmdbId == null) return [];
      
      final seriesDetails = await TmdbApi.getTvDetails(tmdbId, L10n.currentLang);
      if (seriesDetails == null || seriesDetails['seasons'] == null) return [];

      final seasons = seriesDetails['seasons'] as List;
      dynamic currentSeason;
      for (var s in seasons.reversed) {
        if (s['season_number'] > 0) {
          currentSeason = s;
          break;
        }
      }
      
      if (currentSeason == null) return [];

      return await TmdbApi.getSeasonEpisodes(tmdbId, currentSeason['season_number'], L10n.currentLang);
    } catch (e) {
      print('Error fetching air schedule: $e');
      return [];
    }
  }"""

c = re.sub(r"Future<List<dynamic>> _fetchAirSchedule\(\) async \{[\s\S]*?\n  \}", new_fetch, c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated fetch")
