import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Constructor modification
search_ctor = """class PlayerScreen extends StatefulWidget {
  final List<Episode> episodes;
  final int currentEpisodeIndex;
  final String movieName;
  final String? imdbId;
  final int? season;
  final int? episode;
  final bool isLive;

  const PlayerScreen({
    super.key,
    required this.episodes,
    required this.currentEpisodeIndex,
    required this.movieName,
    this.imdbId,
    this.season,
    this.episode,
    this.isLive = false,
  });"""
new_ctor = """class PlayerScreen extends StatefulWidget {
  final List<Episode> episodes;
  final int currentEpisodeIndex;
  final String movieName;
  final String? imdbId;
  final int? season;
  final int? episode;
  final bool isLive;
  final String? lazyPlaylistUrl;

  const PlayerScreen({
    super.key,
    required this.episodes,
    required this.currentEpisodeIndex,
    required this.movieName,
    this.imdbId,
    this.season,
    this.episode,
    this.isLive = false,
    this.lazyPlaylistUrl,
  });"""
content = content.replace(search_ctor, new_ctor)

# 2. Add State variables
search_state = """  // media_kit state
  Duration _position = Duration.zero;"""
new_state = """  bool _isScrapingPlaylist = false;
  WebviewController? _bgWebviewController;
  
  // media_kit state
  Duration _position = Duration.zero;"""
content = content.replace(search_state, new_state)

# 3. Add to initState
search_init = """    _focusNode.requestFocus();
    _startHideControlsTimer();
    _loadSettingsAndInit();"""
new_init = """    _focusNode.requestFocus();
    _startHideControlsTimer();
    _loadSettingsAndInit();
    
    if (widget.lazyPlaylistUrl != null) {
      _startLazyPlaylistScraping(widget.lazyPlaylistUrl!);
    }"""
content = content.replace(search_init, new_init)

# 4. Add _startLazyPlaylistScraping method
new_method = """
  Future<void> _startLazyPlaylistScraping(String url) async {
    final prefs = await SharedPreferences.getInstance();
    final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
    if (!isYtLinked) return;
    
    setState(() { _isScrapingPlaylist = true; });
    
    try {
      final appDataDir = await getApplicationSupportDirectory();
      final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
      try { await WebviewController.initializeEnvironment(userDataPath: profileDir); } catch(e){}
      
      _bgWebviewController = WebviewController();
      await _bgWebviewController!.initialize();
      await _bgWebviewController!.loadUrl(url);
      
      if (mounted) setState(() {});
      
      for (int i = 0; i < 15; i++) {
        await Future.delayed(const Duration(seconds: 1));
        if (!mounted || _bgWebviewController == null || !_bgWebviewController!.value.isInitialized) break;
        
        final js = '''
          (function() {
            var items = document.querySelectorAll('ytd-playlist-panel-video-renderer, ytd-playlist-video-renderer');
            if (items.length === 0) return null;
            var arr = [];
            items.forEach(function(el) {
              var a = el.querySelector('a#wc-endpoint, a.yt-simple-endpoint');
              if (a && a.href) {
                var titleEl = el.querySelector('#video-title');
                var title = titleEl ? titleEl.innerText.trim() : "";
                try {
                  var urlObj = new URL(a.href);
                  var id = urlObj.searchParams.get('v');
                  if (id && title) arr.push({id: id, title: title});
                } catch(e){}
              }
            });
            return arr.length > 0 ? JSON.stringify(arr) : null;
          })();
        ''';
        
        final result = await _bgWebviewController!.executeScript(js) as String?;
        if (result != null && result != "null") {
          final List<dynamic> parsed = jsonDecode(result);
          if (parsed.isNotEmpty) {
            if (mounted) {
              setState(() {
                String currentId = widget.episodes.isNotEmpty ? widget.episodes[_currentIndex].slug : '';
                widget.episodes.clear();
                int newIndex = 0;
                for (int j = 0; j < parsed.length; j++) {
                  var item = parsed[j];
                  widget.episodes.add(Episode(
                    name: item['title'],
                    slug: item['id'],
                    m3u8Url: 'https://www.youtube.com/watch?v=' + item['id']
                  ));
                  if (item['id'] == currentId) newIndex = j;
                }
                _currentIndex = newIndex;
              });
            }
            break;
          }
        }
      }
    } catch(e) {
      print('Lazy Scrape Error: $e');
    } finally {
      if (mounted) setState(() { _isScrapingPlaylist = false; });
      await _bgWebviewController?.dispose();
      _bgWebviewController = null;
    }
  }
"""
# Insert before _dispose
content = content.replace("  @override\n  void dispose() {", new_method + "\n  @override\n  void dispose() {")

# 5. Add Webview to Stack in build
search_stack = """    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (didPop) return;
        _onBackButtonPressed();
      },
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(
          children: ["""
new_stack = """    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (didPop) return;
        _onBackButtonPressed();
      },
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Stack(
          children: [
            if (_bgWebviewController != null && _bgWebviewController!.value.isInitialized)
              Positioned(
                top: -2000,
                left: -2000,
                width: 1280,
                height: 720,
                child: Webview(_bgWebviewController!),
              ),"""
content = content.replace(search_stack, new_stack)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart")
