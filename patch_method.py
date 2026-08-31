import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_method = """
  bool _isScrapingPlaylist = false;
  WebviewController? _bgWebviewController;

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
                    m3u8Url: 'https://www.youtube.com/watch?v=' + item['id'],
                    embedUrl: 'https://i.ytimg.com/vi/' + item['id'] + '/maxresdefault.jpg'
                  ));
                  if (item['id'] == currentId) newIndex = j;
                }
                _currentIndex = newIndex;
                
                final ep = widget.episodes[_currentIndex];
                final epName = ep.name.toLowerCase().startsWith('tập') ? ep.name : 'Tập ${ep.name}';
                _currentTitle = '${widget.movieName} - $epName';
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

if "_startLazyPlaylistScraping(String" not in content:
    content = content.replace("  @override\n  void dispose() {", new_method + "\n  @override\n  void dispose() {", 1)
    
search_stack = """        body: Stack(
          children: ["""
new_stack = """        body: Stack(
          children: [
            if (_bgWebviewController != null && _bgWebviewController!.value.isInitialized)
              Positioned(
                top: 0,
                left: 0,
                width: 1,
                height: 1,
                child: Opacity(
                  opacity: 0.01,
                  child: IgnorePointer(child: Webview(_bgWebviewController!)),
                ),
              ),"""
if "_bgWebviewController != null" not in content:
    content = content.replace(search_stack, new_stack)
    
if "import 'package:path/path.dart' as p;" not in content:
    content = content.replace("import 'package:path_provider/path_provider.dart';", "import 'package:path_provider/path_provider.dart';\nimport 'package:path/path.dart' as p;")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Restored lazy scraping method")
