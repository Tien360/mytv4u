import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import_target = "import '../models/movie.dart';"
if import_target in c:
    c = c.replace(import_target, "import '../models/movie.dart';\nimport '../api/tmdb_api.dart';\nimport 'package:intl/intl.dart';")

badge_target = """                                            _buildBadgeIcon(
                                                Icons.layers,
                                                episodeText,
                                              ),"""

badge_replacement = """                                            _buildBadgeIcon(
                                                Icons.layers,
                                                episodeText,
                                              ),
                                              if (isSeries) ...[
                                                const SizedBox(width: 12),
                                                InkWell(
                                                  onTap: _showAirScheduleModal,
                                                  borderRadius: BorderRadius.circular(6),
                                                  child: Container(
                                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                                    decoration: BoxDecoration(
                                                      color: Colors.white.withOpacity(0.15),
                                                      borderRadius: BorderRadius.circular(6),
                                                      border: Border.all(color: Colors.white.withOpacity(0.3)),
                                                    ),
                                                    child: Row(
                                                      children: [
                                                        const Icon(Icons.calendar_month, color: Colors.blueAccent, size: 16),
                                                        const SizedBox(width: 4),
                                                        Text(L10n.t('air_schedule') ?? 'Lịch phát sóng', style: const TextStyle(color: Colors.blueAccent, fontSize: 13, fontWeight: FontWeight.bold)),
                                                      ],
                                                    ),
                                                  ),
                                                ),
                                              ],"""

if badge_target in c:
    c = c.replace(badge_target, badge_replacement)

# Now add the method
method_target = "  Widget _buildBadgeIcon(IconData icon, String text) {"
method_replacement = """  void _showAirScheduleModal() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1A1A1A),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      isScrollControlled: true,
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.6,
          minChildSize: 0.4,
          maxChildSize: 0.9,
          expand: false,
          builder: (context, scrollController) {
            return FutureBuilder<List<dynamic>>(
              future: _fetchAirSchedule(),
              builder: (context, snapshot) {
                return Column(
                  children: [
                    Container(
                      margin: const EdgeInsets.symmetric(vertical: 12),
                      width: 40,
                      height: 5,
                      decoration: BoxDecoration(
                        color: Colors.white30,
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    Text(
                      L10n.t('air_schedule') ?? 'Lịch phát sóng',
                      style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    Expanded(
                      child: snapshot.connectionState == ConnectionState.waiting
                          ? const Center(child: CircularProgressIndicator(color: Colors.blueAccent))
                          : snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty
                              ? Center(
                                  child: Text(
                                    L10n.t('no_schedule_found') ?? 'Chưa có thông tin lịch chiếu từ TMDB.',
                                    style: const TextStyle(color: Colors.white54),
                                  ),
                                )
                              : ListView.builder(
                                  controller: scrollController,
                                  itemCount: snapshot.data!.length,
                                  padding: const EdgeInsets.symmetric(horizontal: 16),
                                  itemBuilder: (context, index) {
                                    final ep = snapshot.data![index];
                                    final name = ep['name'] ?? 'Tập ${ep['episode_number']}';
                                    final overview = ep['overview'] ?? '';
                                    final airDateStr = ep['air_date'] ?? '';
                                    String formattedDate = airDateStr;
                                    try {
                                      if (airDateStr.isNotEmpty) {
                                        final date = DateTime.parse(airDateStr);
                                        formattedDate = DateFormat('dd/MM/yyyy').format(date);
                                      }
                                    } catch (_) {}
                                    
                                    final stillPath = ep['still_path'];
                                    final thumbUrl = TmdbApi.getImageUrl(stillPath);

                                    return Container(
                                      margin: const EdgeInsets.only(bottom: 16),
                                      decoration: BoxDecoration(
                                        color: Colors.white.withOpacity(0.05),
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: Row(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          ClipRRect(
                                            borderRadius: const BorderRadius.horizontal(left: Radius.circular(12)),
                                            child: thumbUrl.isNotEmpty
                                                ? Image.network(
                                                    thumbUrl,
                                                    width: 120,
                                                    height: 80,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (_, __, ___) => Container(
                                                      width: 120, height: 80, color: Colors.grey[800],
                                                      child: const Icon(Icons.movie, color: Colors.white30),
                                                    ),
                                                  )
                                                : Container(
                                                    width: 120, height: 80, color: Colors.grey[800],
                                                    child: const Icon(Icons.movie, color: Colors.white30),
                                                  ),
                                          ),
                                          const SizedBox(width: 12),
                                          Expanded(
                                            child: Padding(
                                              padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 8.0),
                                              child: Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    'Tập ${ep['episode_number']} - $name',
                                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                                                    maxLines: 1, overflow: TextOverflow.ellipsis,
                                                  ),
                                                  const SizedBox(height: 4),
                                                  Text(
                                                    '${L10n.t('air_date') ?? 'Ngày chiếu'}: $formattedDate',
                                                    style: const TextStyle(color: Colors.blueAccent, fontSize: 12),
                                                  ),
                                                  const SizedBox(height: 4),
                                                  if (overview.isNotEmpty)
                                                    Text(
                                                      overview,
                                                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                                                      maxLines: 2, overflow: TextOverflow.ellipsis,
                                                    ),
                                                ],
                                              ),
                                            ),
                                          )
                                        ],
                                      ),
                                    );
                                  },
                                ),
                    ),
                  ],
                );
              },
            );
          },
        );
      }
    );
  }

  Future<List<dynamic>> _fetchAirSchedule() async {
    if (_movie == null) return [];
    final tmdbId = await TmdbApi.getTmdbTvId(
      imdbId: _movie!.imdbId,
      originalName: _movie!.originalName.isNotEmpty ? _movie!.originalName : _movie!.name,
      year: _movie!.year,
    );
    if (tmdbId == null) return [];
    
    final details = await TmdbApi.getTvDetails(tmdbId, L10n.currentLang);
    if (details == null) return [];
    
    // Tìm season cuối cùng hoặc đang chiếu
    int targetSeason = 1;
    final seasons = details['seasons'] as List?;
    if (seasons != null && seasons.isNotEmpty) {
       // TMDB season 0 thường là Specials. Lấy season có season_number cao nhất > 0.
       int maxS = 1;
       for (var s in seasons) {
         int sn = s['season_number'] ?? 0;
         if (sn > maxS) maxS = sn;
       }
       targetSeason = maxS;
    }
    
    final episodes = await TmdbApi.getSeasonEpisodes(tmdbId, targetSeason, L10n.currentLang);
    return episodes;
  }

  Widget _buildBadgeIcon(IconData icon, String text) {"""

if method_target in c:
    c = c.replace(method_target, method_replacement)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Modified movie_detail_screen.dart")
