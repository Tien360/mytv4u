import re
import os

path = r't:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# We'll inject these methods right before "Widget _buildServerTab"

inject_str = """
  Widget _buildMainTab(String id, String label, IconData icon) {
    final isActive = _activeMainTab == id;
    return GestureDetector(
      onTap: () {
        setState(() {
          _activeMainTab = id;
          if (id == 'Promax') {
            if (_premiumServers.isNotEmpty) _currentServer = _premiumServers.first;
            else if (_p2pServers.isNotEmpty) _currentServer = _p2pServers.first;
            else _currentServer = null;
          } else {
            if (_activeStandardSubTab == 'Vietsub' && _vietsubServers.isNotEmpty) _currentServer = _vietsubServers.first;
            else if (_tmServers.isNotEmpty) _currentServer = _tmServers.first;
            else if (_vietsubServers.isNotEmpty) _currentServer = _vietsubServers.first;
            else _currentServer = null;
          }
          _selectedSeason = null;
          _selectedP2pEpisode = null;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        decoration: BoxDecoration(
          color: isActive ? Colors.redAccent.withOpacity(0.2) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: isActive ? Colors.redAccent : Colors.white.withOpacity(0.1)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: isActive ? Colors.redAccent : Colors.white54, size: 20),
            const SizedBox(width: 8),
            Text(label, style: TextStyle(
              color: isActive ? Colors.white : Colors.white54,
              fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
            )),
          ],
        ),
      ),
    );
  }

  Widget _buildSubTab(String id, String label) {
    final isActive = _activeStandardSubTab == id;
    return GestureDetector(
      onTap: () {
        setState(() {
          _activeStandardSubTab = id;
          if (id == 'Vietsub' && _vietsubServers.isNotEmpty) _currentServer = _vietsubServers.first;
          else if (id == 'Thuyết Minh' && _tmServers.isNotEmpty) _currentServer = _tmServers.first;
          else _currentServer = null;
        });
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          border: Border(bottom: BorderSide(color: isActive ? Colors.blueAccent : Colors.transparent, width: 2)),
        ),
        child: Text(label, style: TextStyle(
          color: isActive ? Colors.white : Colors.white54,
          fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
        )),
      ),
    );
  }

  Widget _buildEpisodesGrid() {
    if (_currentServer == null) return const SizedBox();

    final isP2p = _currentServer!.serverName.toLowerCase().contains('p2p') || _currentServer!.serverName.toLowerCase().contains('torrent');
    
    // For normal servers or P2P Movies (which have items loaded with real streams)
    // Wait, P2P Movies have embedUrl == '' and m3u8Url != 'torrentio://...'?
    // Actually, P2P TV Series have m3u8Url starting with 'torrentio://'.
    bool isP2pSeries = false;
    if (isP2p && _currentServer!.items.isNotEmpty && _currentServer!.items.first.m3u8Url.startsWith('torrentio://')) {
      isP2pSeries = true;
    }

    if (!isP2pSeries) {
      // Normal flat list rendering
      return Wrap(
        spacing: 12,
        runSpacing: 12,
        children: _currentServer!.items.asMap().entries.map((entry) {
          final index = entry.key;
          final ep = entry.value;
          return HoverEpisodeButton(
            text: ep.name,
            onTap: () {
              _pauseTrailer();
              FirebaseApi.saveContinueWatching(_movie!, ep.name);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => PlayerScreen(
                    episodes: _currentServer!.items,
                    currentEpisodeIndex: index,
                    movieName: _movie!.name,
                  )
                )
              );
            },
          );
        }).toList(),
      );
    }

    // P2P TV Series UI: Season -> Episode -> Streams
    // 1. Group items by Season
    final Map<int, List<Episode>> seasonsMap = {};
    for (var ep in _currentServer!.items) {
      // Extract season from slug 'S1E1'
      final match = RegExp(r'S(\d+)E(\d+)').firstMatch(ep.slug);
      if (match != null) {
        final s = int.parse(match.group(1)!);
        seasonsMap.putIfAbsent(s, () => []).add(ep);
      }
    }
    final seasons = seasonsMap.keys.toList()..sort();
    
    if (_selectedSeason == null && seasons.isNotEmpty) {
      _selectedSeason = seasons.first;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Seasons Selector
        const Text('Chọn Mùa:', style: TextStyle(color: Colors.white70)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8, runSpacing: 8,
          children: seasons.map((s) {
            final isActive = _selectedSeason == s;
            return GestureDetector(
              onTap: () => setState(() {
                _selectedSeason = s;
                _selectedP2pEpisode = null;
              }),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: isActive ? Colors.redAccent : Colors.white.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text('Mùa $s', style: TextStyle(color: isActive ? Colors.white : Colors.white70)),
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 24),

        // Episodes Selector
        if (_selectedSeason != null) ...[
          const Text('Chọn Tập:', style: TextStyle(color: Colors.white70)),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8, runSpacing: 8,
            children: seasonsMap[_selectedSeason!]!.map((ep) {
              final isActive = _selectedP2pEpisode == ep;
              return GestureDetector(
                onTap: () => _fetchP2pStreamsForEpisode(ep),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: isActive ? Colors.blueAccent : Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(ep.name, style: TextStyle(color: isActive ? Colors.white : Colors.white70)),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 24),
        ],

        // Streams Display
        if (_selectedP2pEpisode != null) ...[
          const Text('Chọn Luồng phát (Chất lượng):', style: TextStyle(color: Colors.white70)),
          const SizedBox(height: 8),
          if (_isFetchingP2pStreams)
            const Padding(padding: EdgeInsets.all(16), child: CircularProgressIndicator())
          else if (_p2pStreams.isEmpty)
            const Text('Không tìm thấy luồng phát nào cho tập này.', style: TextStyle(color: Colors.redAccent))
          else
            Wrap(
              spacing: 8, runSpacing: 8,
              children: _p2pStreams.asMap().entries.map((entry) {
                final idx = entry.key;
                final stream = entry.value;
                return HoverEpisodeButton(
                  text: stream.name,
                  onTap: () {
                    _pauseTrailer();
                    FirebaseApi.saveContinueWatching(_movie!, '${_selectedP2pEpisode!.slug} - ${stream.name}');
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PlayerScreen(
                          episodes: _p2pStreams,
                          currentEpisodeIndex: idx,
                          movieName: '${_movie!.name} - ${_selectedP2pEpisode!.slug}',
                        )
                      )
                    );
                  },
                );
              }).toList(),
            ),
        ],
      ],
    );
  }

  Future<void> _fetchP2pStreamsForEpisode(Episode ep) async {
    setState(() {
      _selectedP2pEpisode = ep;
      _isFetchingP2pStreams = true;
      _p2pStreams = [];
    });

    try {
      // m3u8Url format: torrentio://imdbId:season:episode
      final parts = ep.m3u8Url.replaceAll('torrentio://', '').split(':');
      if (parts.length == 3) {
        final imdbId = parts[0];
        final season = int.parse(parts[1]);
        final episode = int.parse(parts[2]);
        
        final servers = await TorrentioApi.fetchStreams(imdbId, season: season, episode: episode);
        if (servers.isNotEmpty && mounted) {
          setState(() {
            _p2pStreams = servers.first.items;
          });
        }
      }
    } catch (e) {
      print('Fetch P2P stream error: $e');
    } finally {
      if (mounted) {
        setState(() {
          _isFetchingP2pStreams = false;
        });
      }
    }
  }

"""

insert_idx = content.find("  Widget _buildServerTab")
if insert_idx == -1:
    print("Could not find _buildServerTab")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content[:insert_idx] + inject_str + content[insert_idx:])

print("Successfully injected methods.")
