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

    return Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.all(24.0),
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
            Expanded(
              child: _isLoading
                  ? Center(child: CircularProgressIndicator())
                  : _matches.isEmpty
                      ? Center(
                          child: Text(
                            L10n.t('error_no_matches') ?? 'Không có trận đấu nào.',
                            style: const TextStyle(color: Colors.white70),
                          ),
                        )
                      : RefreshIndicator(
                          onRefresh: _fetchMatches,
                          child: GridView.builder(
                            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                            gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                              maxCrossAxisExtent: 400,
                              childAspectRatio: 2.2,
                              crossAxisSpacing: 16,
                              mainAxisSpacing: 16,
                            ),
                            itemCount: displayMatches.length,
                            itemBuilder: (context, index) {
                              final match = displayMatches[index];
                              return _buildMatchCard(match);
                            },
                          ),
                        ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMatchCard(SportMatch match) {
    final isLive = match.status.toLowerCase() == 'live';
    return GlassContainer(
      borderRadius: 16,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: () => _playMatch(match),
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: isLive ? Colors.red.withOpacity(0.8) : Colors.blue.withOpacity(0.8),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      isLive ? 'LIVE' : match.time,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Expanded(
                    child: Text(
                      match.league,
                      textAlign: TextAlign.right,
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 12,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              const Spacer(),
              Text(
                match.title,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.tv, color: Colors.white54, size: 14),
                  const SizedBox(width: 4),
                  Expanded(
                    child: Text(
                      match.sources.isNotEmpty 
                          ? '${match.sources.length} ${L10n.t('sources_available') ?? "Nguồn phát"}'
                          : L10n.t('error_no_sources_available') ?? 'Không có nguồn',
                      style: const TextStyle(color: Colors.white54, fontSize: 12),
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
