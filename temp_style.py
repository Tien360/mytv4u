import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

modal_ui = """  void _showAirScheduleModal() {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          insetPadding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxHeight: 650),
            child: GlassContainer(
              width: 800,
              borderRadius: 20,
              color: const Color(0xFF141414).withOpacity(0.8),
              borderColor: Colors.white.withOpacity(0.1),
              blur: 40.0,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Header
                  Padding(
                    padding: const EdgeInsets.fromLTRB(30, 24, 24, 16),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.calendar_month_outlined, color: Color(0xFFF59E0B), size: 28),
                            const SizedBox(width: 14),
                            Text(
                              L10n.t('air_schedule') ?? 'Lịch phát sóng',
                              style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold, letterSpacing: 0.5),
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
                  const Divider(color: Colors.white10, height: 1, indent: 30, endIndent: 30),
                  
                  // Content
                  Expanded(
                    child: FutureBuilder<List<dynamic>>(
                      future: _fetchAirSchedule(),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Center(child: CircularProgressIndicator(color: Color(0xFFF59E0B)));
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
                        
                        return ListView.builder(
                          padding: const EdgeInsets.all(30),
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
                              margin: const EdgeInsets.only(bottom: 20),
                              decoration: BoxDecoration(
                                color: Colors.black.withOpacity(0.3),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(color: Colors.white.withOpacity(0.03)),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Thumbnail
                                  ClipRRect(
                                    borderRadius: const BorderRadius.horizontal(left: Radius.circular(16)),
                                    child: SizedBox(
                                      width: 200,
                                      height: 120,
                                      child: thumbUrl.isNotEmpty
                                          ? Image.network(
                                              thumbUrl,
                                              fit: BoxFit.cover,
                                              errorBuilder: (_, __, ___) => _buildFallbackThumb(),
                                            )
                                          : _buildFallbackThumb(),
                                    ),
                                  ),
                                  const SizedBox(width: 24),
                                  // Info
                                  Expanded(
                                    child: Padding(
                                      padding: const EdgeInsets.fromLTRB(0, 20, 20, 20),
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Row(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Expanded(
                                                child: Text(
                                                  'Tập ${ep['episode_number']}: $name',
                                                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 17),
                                                  maxLines: 1, overflow: TextOverflow.ellipsis,
                                                ),
                                              ),
                                              Container(
                                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                decoration: BoxDecoration(
                                                  color: hasPassed ? const Color(0xFFF59E0B).withOpacity(0.15) : Colors.white.withOpacity(0.1),
                                                  borderRadius: BorderRadius.circular(6),
                                                  border: Border.all(color: hasPassed ? const Color(0xFFF59E0B).withOpacity(0.3) : Colors.white.withOpacity(0.1)),
                                                ),
                                                child: Text(
                                                  hasPassed ? 'Đã chiếu' : 'Sắp chiếu',
                                                  style: TextStyle(
                                                    color: hasPassed ? const Color(0xFFF59E0B) : Colors.white70, 
                                                    fontSize: 12, fontWeight: FontWeight.w600, letterSpacing: 0.3
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                          const SizedBox(height: 8),
                                          Row(
                                            children: [
                                              const Icon(Icons.access_time_rounded, color: Colors.white54, size: 15),
                                              const SizedBox(width: 6),
                                              Text(
                                                '${L10n.t('air_date') ?? 'Ngày chiếu'}: $formattedDate',
                                                style: const TextStyle(color: Colors.white70, fontSize: 13),
                                              ),
                                            ],
                                          ),
                                          const SizedBox(height: 12),
                                          if (overview.isNotEmpty)
                                            Text(
                                              overview,
                                              style: const TextStyle(color: Colors.white54, fontSize: 13, height: 1.5),
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
          ),
        );
      }
    );
  }"""

c = re.sub(r"void _showAirScheduleModal\(\) \{[\s\S]*?Widget _buildFallbackThumb\(\)", modal_ui + "\n\n  Widget _buildFallbackThumb()", c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated modal UI style")
