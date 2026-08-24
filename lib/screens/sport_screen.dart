import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../api/sport_api.dart';
import '../models/sport_match.dart';
import '../models/movie.dart';
import '../widgets/glass_container.dart';
import '../utils/l10n.dart';
import 'player_screen.dart';
import 'dart:ui';


class SportScreen extends StatefulWidget {
  const SportScreen({super.key});

  @override
  State<SportScreen> createState() => SportScreenState();
}

class SportScreenState extends State<SportScreen> {
  String _searchQuery = "";
  List<SportMatch> _matches = [];
  bool _isLoading = true;

  void performSearch(String query) {
    if (mounted) {
      setState(() {
        _searchQuery = query;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _fetchMatches();
  }

  Future<void> _fetchMatches() async {
    setState(() => _isLoading = true);
    final matches = await SportApi.getMatches();
    if (mounted) {
      setState(() {
        _matches = matches;
        _isLoading = false;
      });
    }
  }

  void _playMatch(SportMatch match) {
    if (match.sources.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(L10n.t('error_no_sources_available') ?? 'Không có nguồn phát cho trận đấu này!')),
      );
      return;
    }

    final episodes = match.sources.map((s) => Episode(
      name: s.name,
      slug: s.name,
      m3u8Url: s.link,
      embedUrl: s.link,
    )).toList();

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PlayerScreen(
          episodes: episodes,
          currentEpisodeIndex: 0,
          movieName: match.title,
          isLive: true,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final displayMatches = _searchQuery.isEmpty 
        ? _matches 
        : _matches.where((m) => m.title.toLowerCase().contains(_searchQuery.toLowerCase()) || 
                                m.league.toLowerCase().contains(_searchQuery.toLowerCase())).toList();

    final liveMatches = displayMatches.where((m) => m.status.toLowerCase() == 'live').toList();
    final upcomingMatches = displayMatches.where((m) => m.status.toLowerCase() != 'live').toList();

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 24.0, right: 24.0, top: 24.0, bottom: 8.0),
                child: Row(
                  children: [
                    Text(
                      L10n.t('nav_sport') ?? 'Thể Thao',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(width: 16),
                    if (_isLoading)
                      const SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    else
                      IconButton(
                        icon: const Icon(Icons.refresh, color: Colors.white70),
                        onPressed: _fetchMatches,
                        tooltip: L10n.t('refresh'),
                      ),
                  ],
                ),
              ),
              TabBar(
                isScrollable: true,
                indicatorColor: Colors.blueAccent,
                labelColor: Colors.blueAccent,
                unselectedLabelColor: Colors.white54,
                tabs: const [
                  Tab(text: "Đang diễn ra (Live)"),
                  Tab(text: "Sắp diễn ra"),
                  Tab(text: "Lịch Thi Đấu & Tỷ Số"),
                ],
              ),
              Expanded(
                child: TabBarView(
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    _buildMatchGrid(liveMatches, 'Không có trận đấu nào đang diễn ra.'),
                    _buildMatchGrid(upcomingMatches, 'Không có trận đấu nào sắp diễn ra.'),
                    const SportLivescoreWidget(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMatchGrid(List<SportMatch> matches, String emptyMessage) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (matches.isEmpty) {
      return Center(
        child: Text(
          emptyMessage,
          style: const TextStyle(color: Colors.white70),
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: _fetchMatches,
      child: GridView.builder(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
          maxCrossAxisExtent: 400,
          childAspectRatio: 2.2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
        ),
        itemCount: matches.length,
        itemBuilder: (context, index) {
          return _buildMatchCard(matches[index]);
        },
      ),
    );
  }

  Widget _buildMatchCard(SportMatch match) {
    final isLive = match.status.toLowerCase() == 'live';
    
    // Parse teams
    String teamHome = '';
    String teamAway = '';
    bool hasVs = false;
    
    if (match.title.toLowerCase().contains(' vs ')) {
      final parts = match.title.split(RegExp(r' vs ', caseSensitive: false));
      if (parts.length >= 2) {
        teamHome = parts[0].trim();
        teamAway = parts[1].trim();
        hasVs = true;
      }
    }

    return GlassContainer(
      borderRadius: 16,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: () => _playMatch(match),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: isLive ? Colors.redAccent.withValues(alpha: 0.3) : Colors.white10,
              width: 1,
            ),
            gradient: isLive ? LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Colors.redAccent.withValues(alpha: 0.05),
                Colors.transparent,
              ]
            ) : null,
          ),
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Header: League & Status
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      match.league,
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (isLive)
                    Row(
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: Colors.redAccent,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 4),
                        const Text(
                          'LIVE',
                          style: TextStyle(
                            color: Colors.redAccent,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    )
                  else
                    Text(
                      match.time,
                      style: const TextStyle(
                        color: Colors.blueAccent,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                ],
              ),
              const Spacer(),
              
              // Teams
              if (hasVs)
                Row(
                  children: [
                    Expanded(
                      flex: 4,
                      child: Text(
                        teamHome,
                        textAlign: TextAlign.right,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const Expanded(
                      flex: 2,
                      child: Center(
                        child: Text(
                          'VS',
                          style: TextStyle(
                            color: Colors.white30,
                            fontSize: 14,
                            fontWeight: FontWeight.w900,
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      flex: 4,
                      child: Text(
                        teamAway,
                        textAlign: TextAlign.left,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                )
              else
                Text(
                  match.title,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                
              const Spacer(),
              
              // Footer: Sources
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    match.sources.isNotEmpty ? Icons.play_circle_fill : Icons.block,
                    color: match.sources.isNotEmpty ? Colors.white54 : Colors.redAccent.withValues(alpha: 0.5),
                    size: 14,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    match.sources.isNotEmpty 
                        ? '${match.sources.length} Nguồn phát'
                        : 'Chưa có nguồn',
                    style: TextStyle(
                      color: match.sources.isNotEmpty ? Colors.white54 : Colors.redAccent.withValues(alpha: 0.5), 
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

}

class SportLivescoreWidget extends StatefulWidget {
  const SportLivescoreWidget({Key? key}) : super(key: key);

  @override
  State<SportLivescoreWidget> createState() => _SportLivescoreWidgetState();
}

class _SportLivescoreWidgetState extends State<SportLivescoreWidget> with AutomaticKeepAliveClientMixin {
  LivescoreData? _data;
  bool _isLoading = true;
  int _activeLeagueIndex = 0;

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    setState(() => _isLoading = true);
    final data = await SportApi.getLiveScores();
    if (mounted) {
      setState(() {
        _data = data;
        _isLoading = false;
        if (_data != null && _activeLeagueIndex >= _data!.leagues.length) {
          _activeLeagueIndex = 0;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    
    if (_isLoading && _data == null) {
      return const Center(child: CircularProgressIndicator());
    }
    
    if (_data == null || _data!.leagues.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.info_outline, color: Colors.white54, size: 48),
            const SizedBox(height: 16),
            const Text('Không có dữ liệu lịch thi đấu.', style: TextStyle(color: Colors.white70)),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _fetchData,
              child: const Text('Thử lại'),
            ),
          ],
        ),
      );
    }
    
    final leagues = _data!.leagues;

    return Column(
      children: [
        // League Tabs
        Container(
          height: 50,
          margin: const EdgeInsets.only(top: 16),
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 24),
            itemCount: leagues.length,
            itemBuilder: (context, index) {
              final isActive = index == _activeLeagueIndex;
              return Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ChoiceChip(
                  label: Text(leagues[index].leagueName),
                  selected: isActive,
                  onSelected: (selected) {
                    if (selected) setState(() => _activeLeagueIndex = index);
                  },
                  selectedColor: Colors.blueAccent,
                  backgroundColor: Colors.white10,
                  labelStyle: TextStyle(
                    color: isActive ? Colors.white : Colors.white70,
                    fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              );
            },
          ),
        ),
        
        // Last update text
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Cập nhật: ${_data!.lastUpdate}',
                style: const TextStyle(color: Colors.white54, fontSize: 12),
              ),
              IconButton(
                icon: const Icon(Icons.refresh, color: Colors.white54, size: 20),
                onPressed: _fetchData,
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
              ),
            ],
          ),
        ),
        
        // Matches List
        Expanded(
          child: RefreshIndicator(
            onRefresh: _fetchData,
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
              itemCount: leagues[_activeLeagueIndex].days.length,
              itemBuilder: (context, dayIndex) {
                final day = leagues[_activeLeagueIndex].days[dayIndex];
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Day Header
                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                      margin: const EdgeInsets.only(top: 16, bottom: 8),
                      decoration: BoxDecoration(
                        color: Colors.white10,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.calendar_today, color: Colors.blueAccent, size: 16),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              day.date,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    
                    // Matches
                    ...day.matches.map((match) {
                      bool isFinished = match.status == 'FT' || match.status == 'Finished' || match.status == 'played';
                      String displayScore = match.score.isNotEmpty ? match.score : (isFinished ? '?' : 'vs');
                      
                      return Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.black26,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.white10),
                        ),
                        child: Row(
                          children: [
                            // Time
                            SizedBox(
                              width: 80,
                              child: Text(
                                match.time.replaceAll('<br>', ' '),
                                style: TextStyle(
                                  color: isFinished ? Colors.white54 : Colors.blueAccent,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            
                            // Teams & Score
                            Expanded(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Expanded(
                                    child: Text(
                                      match.teamHome,
                                      textAlign: TextAlign.right,
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontWeight: isFinished ? FontWeight.normal : FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                    margin: const EdgeInsets.symmetric(horizontal: 12),
                                    decoration: BoxDecoration(
                                      color: isFinished ? Colors.white10 : Colors.redAccent.withValues(alpha: 0.8),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      displayScore,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    child: Text(
                                      match.teamAway,
                                      textAlign: TextAlign.left,
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontWeight: isFinished ? FontWeight.normal : FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    }).toList(),
                  ],
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}
