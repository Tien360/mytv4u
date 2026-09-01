import 'package:flutter/material.dart';
import '../api/tmdb_api.dart';
import '../api/translate_api.dart';
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
          _error = L10n.t('error_tmdb_id_not_found');
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
          _error = L10n.t('error_no_seasons');
          _isLoading = false;
        });
        return;
      }

      _validSeasons = seasons.where((s) => s['season_number'] > 0).toList();
      if (_validSeasons.isEmpty) {
        setState(() {
          _error = L10n.t('error_no_valid_seasons');
          _isLoading = false;
        });
        return;
      }

      _selectedSeasonNumber = _validSeasons.last['season_number'];
      await _fetchEpisodesForSeason(_selectedSeasonNumber!);
    } catch (e) {
      setState(() {
        _error = '${L10n.t('error_prefix')}: $e';
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
        _error = '${L10n.t('error_loading_episodes')}: $e';
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
                          L10n.t('air_schedule'),
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
                                    child: Text(s['name'] ?? '${L10n.t('season')} ${s['season_number']}'),
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
                                  L10n.t('no_schedule_found'),
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
  bool _isTranslating = false;
  bool _showOriginal = false;
  String? _translatedOverview;

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
    final name = ep['name'] ?? '${L10n.t('episode')} ${ep['episode_number']}';
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
    
    final createdBy = widget.mainSeriesDetails['created_by'] as List<dynamic>? ?? [];
    final createdByNames = createdBy.map((c) => c['name']).toSet();
    final validDirectors = directors.where((d) => !createdByNames.contains(d['name'])).toList();
    
    
    List<Map<String, dynamic>> crewList = [];
    for (var d in validDirectors) {
      crewList.add({
        'name': d['name'] ?? '',
        'role': L10n.t('director'),
        'profile_path': d['profile_path'] ?? '',
      });
    }
    for (var w in writers) {
      crewList.add({
        'name': w['name'] ?? '',
        'role': L10n.t('writer'),
        'profile_path': w['profile_path'] ?? '',
      });
    }
    
    List<Map<String, dynamic>> guestList = [];
    for (var g in guestStars) {
      guestList.add({
        'name': g['name'] ?? '',
        'role': g['character'] ?? '',
        'profile_path': g['profile_path'] ?? '',
      });
    }
    
    return GestureDetector(
      onTap: () async {
        setState(() {
          _isExpanded = !_isExpanded;
        });
        if (_isExpanded && widget.ep['_needs_translation'] == true && _translatedOverview == null && !_isTranslating) {
          setState(() { _isTranslating = true; });
          final res = await TranslateApi.translateEnToVi(widget.ep['overview'] ?? '');
          if (mounted) {
            setState(() {
              _translatedOverview = res;
              _isTranslating = false;
            });
          }
        }
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
                                '${L10n.t('episode')} ${ep['episode_number']}: $name',
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
                                hasPassed ? L10n.t('released') : L10n.t('upcoming'),
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
                              '${L10n.t('air_date')}: $formattedDate',
                              style: const TextStyle(color: Colors.white70, fontSize: 13),
                            ),
                            const SizedBox(width: 16),
                            if (ep['runtime'] != null) ...[
                              const Icon(Icons.timer_outlined, color: Colors.white54, size: 15),
                              const SizedBox(width: 6),
                              Text(
                                '${ep['runtime']} ${L10n.t('minutes')}',
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
                                    '(${ep['vote_count'] ?? 0} ${L10n.t('votes')})',
                                    style: const TextStyle(color: Colors.white54, fontSize: 12),
                                  ),
                                ],
                              ),
                            ),
                          
                          if (overview.isNotEmpty)
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  (_translatedOverview != null && !_showOriginal) ? _translatedOverview! : overview,
                                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                                ),
                                if (_isTranslating)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8),
                                    child: Row(
                                      children: [
                                        const SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFFF59E0B))),
                                        const SizedBox(width: 8),
                                        Text(L10n.t('translating'), style: TextStyle(color: Colors.white54, fontSize: 12, fontStyle: FontStyle.italic)),
                                      ],
                                    ),
                                  ),
                                if (_translatedOverview != null && widget.ep['_needs_translation'] == true)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8),
                                    child: Row(
                                      children: [
                                        const Icon(Icons.g_translate, color: Colors.white30, size: 14),
                                        const SizedBox(width: 6),
                                        Text(L10n.t('translated_by_google'), style: const TextStyle(color: Colors.white30, fontSize: 12, fontStyle: FontStyle.italic)),
                                        const Spacer(),
                                        GestureDetector(
                                          onTap: () {
                                            setState(() { _showOriginal = !_showOriginal; });
                                          },
                                          child: Text(
                                            _showOriginal ? L10n.t('show_translation') : L10n.t('show_original'),
                                            style: const TextStyle(color: Color(0xFFF59E0B), fontSize: 12, fontWeight: FontWeight.w500),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                              ],
                            ),
                            
                          const SizedBox(height: 16),
                          
                          // Crew & Guests
                          if (crewList.isNotEmpty) 
                            HorizontalAvatarList(title: '${L10n.t('director')} & ${L10n.t('writer')}', items: crewList),
                          if (guestList.isNotEmpty)
                            HorizontalAvatarList(title: L10n.t('guest_stars'), items: guestList),

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


class HorizontalAvatarList extends StatefulWidget {
  final String title;
  final List<Map<String, dynamic>> items;

  const HorizontalAvatarList({super.key, required this.title, required this.items});

  @override
  State<HorizontalAvatarList> createState() => _HorizontalAvatarListState();
}

class _HorizontalAvatarListState extends State<HorizontalAvatarList> {
  final ScrollController _scrollController = ScrollController();
  bool _canScrollLeft = false;
  bool _canScrollRight = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_updateScrollButtons);
    WidgetsBinding.instance.addPostFrameCallback((_) => _updateScrollButtons());
  }

  void _updateScrollButtons() {
    if (!_scrollController.hasClients) return;
    setState(() {
      _canScrollLeft = _scrollController.position.pixels > 0;
      _canScrollRight = _scrollController.position.pixels < _scrollController.position.maxScrollExtent;
    });
  }

  void _scrollLeft() {
    _scrollController.animateTo(
      (_scrollController.position.pixels - 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  void _scrollRight() {
    _scrollController.animateTo(
      (_scrollController.position.pixels + 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  @override
  void dispose() {
    _scrollController.removeListener(_updateScrollButtons);
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.items.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 16),
        Text(
          widget.title,
          style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 140,
          child: Stack(
            children: [
              ListView.builder(
                controller: _scrollController,
                scrollDirection: Axis.horizontal,
                itemCount: widget.items.length,
                itemBuilder: (context, idx) {
                  final person = widget.items[idx];
                  final profilePath = person['profile_path'];
                  final profileUrl = TmdbApi.getImageUrl(profilePath);
                  return Container(
                    width: 90,
                    margin: const EdgeInsets.only(right: 12),
                    child: Column(
                      children: [
                        CircleAvatar(
                          radius: 35,
                          backgroundColor: Colors.white.withValues(alpha: 0.1),
                          backgroundImage: profileUrl.isNotEmpty ? NetworkImage(profileUrl) : null,
                          child: profileUrl.isEmpty ? const Icon(Icons.person, color: Colors.white30) : null,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          person['name'] ?? '',
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          person['role'] ?? '',
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
              if (_canScrollLeft)
                Positioned(
                  left: 0,
                  top: 0,
                  bottom: 30,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.black.withValues(alpha: 0.6),
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_left, color: Colors.white),
                        onPressed: _scrollLeft,
                      ),
                    ),
                  ),
                ),
              if (_canScrollRight)
                Positioned(
                  right: 0,
                  top: 0,
                  bottom: 30,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.black.withValues(alpha: 0.6),
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_right, color: Colors.white),
                        onPressed: _scrollRight,
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}
