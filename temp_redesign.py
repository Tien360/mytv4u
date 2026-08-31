import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

pattern = r"void _showAirScheduleModal\(\).*?Future<List<dynamic>> _fetchAirSchedule\(\) async \{"
replacement = r"""void _showAirScheduleModal() {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          insetPadding: const EdgeInsets.all(24),
          child: Container(
            width: 800,
            constraints: const BoxConstraints(maxHeight: 650),
            decoration: BoxDecoration(
              color: const Color(0xFF141414).withOpacity(0.95),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white.withOpacity(0.1)),
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 20, spreadRadius: 5),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 24, 24, 16),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.calendar_month, color: Colors.blueAccent, size: 28),
                          const SizedBox(width: 12),
                          Text(
                            L10n.t('air_schedule') ?? 'Lịch phát sóng',
                            style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white70),
                        onPressed: () => Navigator.pop(context),
                        hoverColor: Colors.white10,
                        splashRadius: 24,
                      ),
                    ],
                  ),
                ),
                const Divider(color: Colors.white10, height: 1),
                
                // Content
                Expanded(
                  child: FutureBuilder<List<dynamic>>(
                    future: _fetchAirSchedule(),
                    builder: (context, snapshot) {
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
                      
                      return ListView.builder(
                        padding: const EdgeInsets.all(24),
                        itemCount: snapshot.data!.length,
                        itemBuilder: (context, index) {
                          final ep = snapshot.data![index];
                          final name = ep['name'] ?? 'Tập ${ep['episode_number']}';
                          final overview = ep['overview'] ?? '';
                          final airDateStr = ep['air_date'] ?? '';
                          String formattedDate = airDateStr;
                          try {
                            if (airDateStr.isNotEmpty) {
                              final date = DateTime.parse(airDateStr);
                              formattedDate = '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
                            }
                          } catch (_) {}
                          
                          final stillPath = ep['still_path'];
                          final thumbUrl = TmdbApi.getImageUrl(stillPath);
                          final bool hasPassed = airDateStr.isNotEmpty && DateTime.parse(airDateStr).isBefore(DateTime.now());

                          return Container(
                            margin: const EdgeInsets.only(bottom: 16),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.03),
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: Colors.white.withOpacity(0.05)),
                            ),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Thumbnail
                                ClipRRect(
                                  borderRadius: const BorderRadius.horizontal(left: Radius.circular(12)),
                                  child: SizedBox(
                                    width: 180,
                                    height: 110,
                                    child: thumbUrl.isNotEmpty
                                        ? Image.network(
                                            thumbUrl,
                                            fit: BoxFit.cover,
                                            errorBuilder: (_, __, ___) => _buildFallbackThumb(),
                                          )
                                        : _buildFallbackThumb(),
                                  ),
                                ),
                                const SizedBox(width: 20),
                                // Info
                                Expanded(
                                  child: Padding(
                                    padding: const EdgeInsets.fromLTRB(0, 16, 16, 16),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Expanded(
                                              child: Text(
                                                'Tập ${ep['episode_number']}: $name',
                                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                                                maxLines: 1, overflow: TextOverflow.ellipsis,
                                              ),
                                            ),
                                            Container(
                                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                              decoration: BoxDecoration(
                                                color: hasPassed ? Colors.green.withOpacity(0.15) : Colors.orange.withOpacity(0.15),
                                                borderRadius: BorderRadius.circular(4),
                                              ),
                                              child: Text(
                                                hasPassed ? 'Đã chiếu' : 'Sắp chiếu',
                                                style: TextStyle(
                                                  color: hasPassed ? Colors.greenAccent : Colors.orangeAccent, 
                                                  fontSize: 11, fontWeight: FontWeight.bold
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 6),
                                        Row(
                                          children: [
                                            const Icon(Icons.access_time, color: Colors.white54, size: 14),
                                            const SizedBox(width: 6),
                                            Text(
                                              '${L10n.t('air_date') ?? 'Ngày chiếu'}: $formattedDate',
                                              style: const TextStyle(color: Colors.white70, fontSize: 13),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 10),
                                        if (overview.isNotEmpty)
                                          Text(
                                            overview,
                                            style: const TextStyle(color: Colors.white54, fontSize: 13, height: 1.4),
                                            maxLines: 2, overflow: TextOverflow.ellipsis,
                                          ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        );
      }
    );
  }

  Widget _buildFallbackThumb() {
    return Container(
      color: Colors.black26,
      child: const Center(
        child: Icon(Icons.movie, color: Colors.white24, size: 32),
      ),
    );
  }

  Future<List<dynamic>> _fetchAirSchedule() async {"""

if re.search(pattern, c, re.DOTALL):
    c = re.sub(pattern, replacement, c, flags=re.DOTALL)
    print("Redesigned UI")
else:
    print("Pattern not found")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

