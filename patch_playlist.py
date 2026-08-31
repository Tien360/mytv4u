import re

def patch_playlist(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace widget.episodes with _episodes
    content = content.replace("widget.episodes", "_episodes")
    
    # 2. But we need to initialize _episodes in state
    state_injection = '''
  List<Episode> _episodes = [];
  bool _isLoadingPlaylist = false;
'''
    content = content.replace("bool _isPlayerInitialized = false;", "bool _isPlayerInitialized = false;\n" + state_injection)
    
    # 3. In initState, populate _episodes and call load
    init_injection = '''
    _episodes = List.from(widget.episodes);
    if (widget.lazyPlaylistUrl != null) {
      _loadLazyPlaylist(widget.lazyPlaylistUrl!);
    }
'''
    content = content.replace("windowManager.addListener(this);", "windowManager.addListener(this);\n" + init_injection)
    
    # 4. _loadLazyPlaylist method
    load_method = '''
  Future<void> _loadLazyPlaylist(String url) async {
    setState(() => _isLoadingPlaylist = true);
    try {
      final res = await Process.run('yt-dlp', ['--dump-json', '--flat-playlist', url]);
      if (res.exitCode == 0) {
        final lines = res.stdout.toString().split('\\n').where((l) => l.trim().isNotEmpty).toList();
        final List<Episode> newEps = [];
        for (var line in lines) {
          try {
            final json = jsonDecode(line);
            final title = json['title'] ?? 'Video';
            final id = json['id'] ?? '';
            if (id.isNotEmpty) {
              newEps.add(Episode(
                name: title,
                slug: id,
                m3u8Url: 'https://www.youtube.com/watch?v=\',
                embedUrl: 'https://i.ytimg.com/vi/\/maxresdefault.jpg'
              ));
            }
          } catch(e) {}
        }
        if (mounted && newEps.isNotEmpty) {
          setState(() {
            _episodes = newEps;
            // Also update the current episode name if we were on the first dummy one
            if (_currentIndex < _episodes.length && _episodes[_currentIndex].name.contains('loading')) {
               _episodes[_currentIndex].name = newEps[0].name;
            }
          });
        }
      }
    } catch (e) {
      debugPrint('Playlist load error: \');
    }
    if (mounted) setState(() => _isLoadingPlaylist = false);
  }
'''
    # insert before _fetchYoutubeQualities
    content = content.replace("Future<void> _fetchYoutubeQualities", load_method + "\n  Future<void> _fetchYoutubeQualities")
    
    # 5. Extract title in _fetchYoutubeQualities
    title_inj = '''
          if (data['title'] != null && _currentIndex >= 0 && _currentIndex < _episodes.length) {
            _episodes[_currentIndex].name = data['title'];
          }
'''
    content = content.replace("final formats = data['formats'] as List;", title_inj + "\n          final formats = data['formats'] as List;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_playlist('lib/screens/player_screen.dart')
print("Patched playlist logic")
