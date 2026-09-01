import 'package:flutter/material.dart';
import '../api/tmdb_api.dart';
import '../utils/l10n.dart';
import 'glass_container.dart';

class AirScheduleDialog extends StatefulWidget {
  final Map<String, dynamic> tmdbDetails;

  const AirScheduleDialog({super.key, required this.tmdbDetails});

  @override
  State<AirScheduleDialog> createState() => _AirScheduleDialogState();
}

class _AirScheduleDialogState extends State<AirScheduleDialog> {
  List<dynamic> _validSeasons = [];
  int? _selectedSeasonNumber;
  List<dynamic>? _episodes;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _initData();
  }

  Future<void> _initData() async {
    try {
      final tmdbId = int.tryParse(widget.tmdbDetails['id']?.toString() ?? '');
      if (tmdbId == null) {
        setState(() {
          _error = 'Không tìm thấy ID TMDB';
          _isLoading = false;
        });
        return;
      }

      List? seasons = widget.tmdbDetails['seasons'] as List?;
      if (seasons == null || seasons.isEmpty) {
        final seriesDetails = await TmdbApi.getTvDetails(tmdbId, L10n.currentLang);
        seasons = seriesDetails?['seasons'] as List?;
      }

      if (seasons == null || seasons.isEmpty) {
        setState(() {
          _error = 'Không có thông tin các Phần (Seasons).';
          _isLoading = false;
        });
        return;
      }

      _validSeasons = seasons.where((s) => s['season_number'] > 0).toList();
      if (_validSeasons.isEmpty) {
        setState(() {
          _error = 'Phim chưa có phần nào hợp lệ.';
          _isLoading = false;
        });
        return;
      }

      // Default to latest season
      _selectedSeasonNumber = _validSeasons.last['season_number'];
      await _fetchEpisodesForSeason(_selectedSeasonNumber!);
    } catch (e) {
      setState(() {
        _error = 'Lỗi: $e';
        _isLoading = false;
      });
    }
  }

  Future<void> _fetchEpisodesForSeason(int seasonNumber) async {
    setState(() {
      _isLoading = true;
      _error = null;
    });
    try {
      final tmdbId = int.tryParse(widget.tmdbDetails['id']?.toString() ?? '');
      final eps = await TmdbApi.getSeasonEpisodes(tmdbId!, seasonNumber, L10n.currentLang);
      setState(() {
        _episodes = eps;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Lỗi tải tập phim: $e';
        _isLoading = false;
      });
    }
  }

  Widget _buildFallbackThumb() {
    return Container(
      color: Colors.white.withOpacity(0.05),
      child: const Center(
        child: Icon(Icons.movie_outlined, color: Colors.white24, size: 40),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
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
                          style: const TextStyle(
                              color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold, letterSpacing: 0.5),
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        if (_validSeasons.length > 1)
                          Container(
                            margin: const EdgeInsets.only(right: 16),
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.white.withOpacity(0.2)),
                            ),
                            child: DropdownButtonHideUnderline(
                              child: DropdownButton<int>(
                                value: _selectedSeasonNumber,
                                dropdownColor: const Color(0xFF1E1E1E),
                                icon: const Icon(Icons.arrow_drop_down, color: Colors.white70),
                                style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w500),
                                items: _validSeasons.map((s) {
                                  return DropdownMenuItem<int>(
                                    value: s['season_number'],
                                    child: Text(s['name'] ?? 'Phần ${s['season_number']}'),
                                  );
                                }).toList(),
                                onChanged: (val) {
                                  if (val != null && val != _selectedSeasonNumber) {
                                    setState(() {
                                      _selectedSeasonNumber = val;
                                    });
                                    _fetchEpisodesForSeason(val);
                                  }
                                },
                              ),
                            ),
                          ),
                        IconButton(
                          icon: const Icon(Icons.close, color: Colors.white70),
                          onPressed: () => Navigator.pop(context),
                          hoverColor: Colors.white10,
                          splashRadius: 24,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const Divider(color: Colors.white10, height: 1, indent: 30, endIndent: 30),

              // Content
              Expanded(
                child: _isLoading
                    ? const Center(child: CircularProgressIndicator(color: Color(0xFFF59E0B)))
                    : _error != null
                        ? Center(
                            child: Text(
                              _error!,
                              style: const TextStyle(color: Colors.redAccent, fontSize: 16),
                            ),
                          )
                        : (_episodes == null || _episodes!.isEmpty)
                            ? Center(
                                child: Text(
                                  L10n.t('no_schedule_found') ?? 'Chưa có thông tin lịch chiếu từ TMDB.',
                                  style: const TextStyle(color: Colors.white54, fontSize: 16),
                                ),
                              )
                            : ListView.builder(
                                padding: const EdgeInsets.all(30),
                                itemCount: _episodes!.length,
                                itemBuilder: (context, index) {
                                  final ep = _episodes![index];
                                  final name = ep['name'] ?? 'Tập ${ep['episode_number']}';
                                  final overview = ep['overview'] ?? '';
                                  final airDateStr = ep['air_date'] ?? '';
                                  String formattedDate = airDateStr;
                                  try {
                                    if (airDateStr.isNotEmpty) {
                                      final date = DateTime.parse(airDateStr);
                                      formattedDate =
                                          '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
                                    }
                                  } catch (_) {}

                                  final stillPath = ep['still_path'];
                                  final thumbUrl = TmdbApi.getImageUrl(stillPath);
                                  final bool hasPassed = airDateStr.isNotEmpty &&
                                      DateTime.parse(airDateStr).isBefore(DateTime.now());

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
                                                        style: const TextStyle(
                                                            color: Colors.white,
                                                            fontWeight: FontWeight.bold,
                                                            fontSize: 17),
                                                        maxLines: 1,
                                                        overflow: TextOverflow.ellipsis,
                                                      ),
                                                    ),
                                                    const SizedBox(width: 12),
                                                    Container(
                                                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                      decoration: BoxDecoration(
                                                        color: hasPassed
                                                            ? const Color(0xFFF59E0B).withOpacity(0.15)
                                                            : Colors.white.withOpacity(0.1),
                                                        borderRadius: BorderRadius.circular(6),
                                                        border: Border.all(
                                                            color: hasPassed
                                                                ? const Color(0xFFF59E0B).withOpacity(0.3)
                                                                : Colors.white.withOpacity(0.1)),
                                                      ),
                                                      child: Text(
                                                        hasPassed ? 'Đã chiếu' : 'Sắp chiếu',
                                                        style: TextStyle(
                                                            color: hasPassed ? const Color(0xFFF59E0B) : Colors.white70,
                                                            fontSize: 12,
                                                            fontWeight: FontWeight.w600,
                                                            letterSpacing: 0.3),
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                                const SizedBox(height: 8),
                                                Row(
                                                  children: [
                                                    const Icon(Icons.access_time_rounded,
                                                        color: Colors.white54, size: 15),
                                                    const SizedBox(width: 6),
                                                    Text(
                                                      '${L10n.t('air_date') ?? 'Ngày chiếu'}: $formattedDate',
                                                      style: const TextStyle(color: Colors.white70, fontSize: 13),
                                                    ),
                                                    const SizedBox(width: 16),
                                                    if (ep['runtime'] != null) ...[
                                                      const Icon(Icons.timer_outlined, color: Colors.white54, size: 15),
                                                      const SizedBox(width: 6),
                                                      Text(
                                                        '${ep['runtime']} phút',
                                                        style: const TextStyle(color: Colors.white70, fontSize: 13),
                                                      ),
                                                    ]
                                                  ],
                                                ),
                                                if (overview.isNotEmpty) ...[
                                                  const SizedBox(height: 12),
                                                  Text(
                                                    overview,
                                                    style: const TextStyle(
                                                        color: Colors.white60, fontSize: 13, height: 1.5),
                                                    maxLines: 3,
                                                    overflow: TextOverflow.ellipsis,
                                                  ),
                                                ],
                                              ],
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
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
}
