import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

new_fetch = """  Future<List<dynamic>> _fetchAirSchedule() async {
    try {
      final tmdbId = _tmdbDetails != null ? int.tryParse(_tmdbDetails!['id']?.toString() ?? '') : null;
      if (tmdbId == null) return [{'error': 'Không tìm thấy ID TMDB của phim.'}];
      
      List? seasons = _tmdbDetails!['seasons'] as List?;
      if (seasons == null || seasons.isEmpty) {
        final seriesDetails = await TmdbApi.getTvDetails(tmdbId, L10n.currentLang);
        if (seriesDetails != null) {
          seasons = seriesDetails['seasons'] as List?;
        }
      }

      if (seasons == null || seasons.isEmpty) return [{'error': 'Phim không có thông tin các phần (Seasons).'}];

      dynamic currentSeason;
      for (var s in seasons.reversed) {
        if (s['season_number'] > 0) {
          currentSeason = s;
          break;
        }
      }
      
      if (currentSeason == null) return [{'error': 'Phim chưa có phần nào hợp lệ.'}];

      final eps = await TmdbApi.getSeasonEpisodes(tmdbId, currentSeason['season_number'], L10n.currentLang);
      if (eps.isEmpty) {
        return [{'error': 'Phần ${currentSeason['season_number']} chưa có thông tin tập phim.'}];
      }
      return eps;
    } catch (e) {
      return [{'error': 'Lỗi xử lý: $e'}];
    }
  }"""

c = re.sub(r"Future<List<dynamic>> _fetchAirSchedule\(\) async \{[\s\S]*?\n  \}", new_fetch, c)

# update ui to show error if present
ui_builder = """                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return const Center(child: CircularProgressIndicator(color: Colors.blueAccent));
                      }
                      if (snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty) {
                        return Center(
                          child: Text(
                            L10n.t('no_schedule_found') ?? 'Chưa có thông tin lịch chiếu từ TMDB.',
                            style: const TextStyle(color: Colors.white54, fontSize: 16),
                          ),
                        );
                      }

                      final firstItem = snapshot.data!.first;
                      if (firstItem is Map && firstItem.containsKey('error')) {
                        return Center(
                          child: Text(
                            firstItem['error'],
                            style: const TextStyle(color: Colors.redAccent, fontSize: 16),
                          ),
                        );
                      }
                      
                      return ListView.builder("""
                      
c = re.sub(r"                    builder: \(context, snapshot\) \{[\s\S]*?return ListView.builder\(", ui_builder, c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated fetch with debug")
