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

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.all(24),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxHeight: 700),
        child: GlassContainer(
          width: 850,
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
                        const Icon(Icons.menu_book_rounded, color: Color(0xFFF59E0B), size: 28),
                        const SizedBox(width: 14),
                        Text(
                          L10n.t('air_schedule') ?? 'Cẩm nang Tập phim',
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
                                  return ExpandableEpisodeCard(
                                    ep: ep,
                                    mainSeriesDetails: widget.tmdbDetails,
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

class ExpandableEpisodeCard extends StatefulWidget {
  final Map<String, dynamic> ep;
  final Map<String, dynamic> mainSeriesDetails;

  const ExpandableEpisodeCard({super.key, required this.ep, required this.mainSeriesDetails});

  @override
  State<ExpandableEpisodeCard> createState() => _ExpandableEpisodeCardState();
}

class _ExpandableEpisodeCardState extends State<ExpandableEpisodeCard> {
  bool _isExpanded = false;

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
    final ep = widget.ep;
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

    final voteAvg = ep['vote_average'];
    final guestStars = ep['guest_stars'] as List<dynamic>? ?? [];
    
    // Process Crew
    final crew = ep['crew'] as List<dynamic>? ?? [];
    final directors = crew.where((c) => c['job'] == 'Director').toList();
    final writers = crew.where((c) => c['job'] == 'Writer').toList();
    
    // Check if director is the same as main created_by
    final createdBy = widget.mainSeriesDetails['created_by'] as List<dynamic>? ?? [];
    final createdByNames = createdBy.map((c) => c['name']).toSet();
    
    final validDirectors = directors.where((d) => !createdByNames.contains(d['name'])).toList();

    return GestureDetector(
      onTap: () {
        setState(() {
          _isExpanded = !_isExpanded;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        margin: const EdgeInsets.only(bottom: 20),
        decoration: BoxDecoration(
          color: _isExpanded ? const Color(0xFF1E1E1E) : Colors.black.withOpacity(0.3),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
              color: _isExpanded
                  ? const Color(0xFFF59E0B).withOpacity(0.3)
                  : Colors.white.withOpacity(0.05)),
          boxShadow: _isExpanded
              ? [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 10, offset: const Offset(0, 5))]
              : [],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top Row (Always visible)
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Thumbnail
                ClipRRect(
                  borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(16), bottomLeft: Radius.circular(16),
                      bottomRight: Radius.circular(0), topRight: Radius.circular(0)),
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
                                style: TextStyle(
                                    color: _isExpanded ? const Color(0xFFF59E0B) : Colors.white,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18),
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
                            const Icon(Icons.access_time_rounded, color: Colors.white54, size: 15),
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
                            ],
                            const Spacer(),
                            Icon(
                              _isExpanded ? Icons.keyboard_arrow_up_rounded : Icons.keyboard_arrow_down_rounded,
                              color: Colors.white30,
                              size: 24,
                            ),
                          ],
                        ),
                        if (!_isExpanded && overview.isNotEmpty) ...[
                          const SizedBox(height: 12),
                          Text(
                            overview,
                            style: const TextStyle(color: Colors.white60, fontSize: 13, height: 1.5),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            ),
            
            // Expanded Content (AnimatedSize)
            AnimatedSize(
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeInOut,
              alignment: Alignment.topCenter,
              child: !_isExpanded
                  ? const SizedBox.shrink()
                  : Padding(
                      padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Divider(color: Colors.white10, height: 1),
                          const SizedBox(height: 16),
                          
                          // Rating & Full Overview
                          if (voteAvg != null && voteAvg > 0)
                            Padding(
                              padding: const EdgeInsets.only(bottom: 12),
                              child: Row(
                                children: [
                                  const Icon(Icons.star_rounded, color: Colors.amber, size: 18),
                                  const SizedBox(width: 6),
                                  Text(
                                    '${(voteAvg as num).toStringAsFixed(1)}/10',
                                    style: const TextStyle(
                                        color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                                  ),
                                  const SizedBox(width: 4),
                                  Text(
                                    '(${ep['vote_count'] ?? 0} votes)',
                                    style: const TextStyle(color: Colors.white54, fontSize: 12),
                                  ),
                                ],
                              ),
                            ),
                          
                          if (overview.isNotEmpty)
                            Text(
                              overview,
                              style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                            ),
                            
                          const SizedBox(height: 16),
                          
                          // Crew
                          if (validDirectors.isNotEmpty || writers.isNotEmpty)
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.03),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  if (validDirectors.isNotEmpty)
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          const Text('Đạo diễn', style: TextStyle(color: Colors.white54, fontSize: 12)),
                                          const SizedBox(height: 4),
                                          Text(
                                            validDirectors.map((d) => d['name']).join(', '),
                                            style: const TextStyle(color: Colors.white, fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                  if (writers.isNotEmpty)
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          const Text('Biên kịch', style: TextStyle(color: Colors.white54, fontSize: 12)),
                                          const SizedBox(height: 4),
                                          Text(
                                            writers.map((w) => w['name']).join(', '),
                                            style: const TextStyle(color: Colors.white, fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                ],
                              ),
                            ),
                            
                          // Guest Stars
                          if (guestStars.isNotEmpty) ...[
                            const SizedBox(height: 20),
                            const Text(
                              'Diễn viên khách mời',
                              style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w600),
                            ),
                            const SizedBox(height: 12),
                            SizedBox(
                              height: 140,
                              child: ListView.builder(
                                scrollDirection: Axis.horizontal,
                                itemCount: guestStars.length,
                                itemBuilder: (context, idx) {
                                  final actor = guestStars[idx];
                                  final profilePath = actor['profile_path'];
                                  final profileUrl = TmdbApi.getImageUrl(profilePath);
                                  return Container(
                                    width: 90,
                                    margin: const EdgeInsets.only(right: 12),
                                    child: Column(
                                      children: [
                                        CircleAvatar(
                                          radius: 35,
                                          backgroundColor: Colors.white.withOpacity(0.1),
                                          backgroundImage: profileUrl.isNotEmpty ? NetworkImage(profileUrl) : null,
                                          child: profileUrl.isEmpty ? const Icon(Icons.person, color: Colors.white30) : null,
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          actor['name'] ?? '',
                                          textAlign: TextAlign.center,
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500),
                                        ),
                                        const SizedBox(height: 2),
                                        Text(
                                          actor['character'] ?? '',
                                          textAlign: TextAlign.center,
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white54, fontSize: 11),
                                        ),
                                      ],
                                    ),
                                  );
                                },
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
