import re

def fix_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace _loadLazyPlaylist
    old_load = r"Future<void> _loadLazyPlaylist\(String url\) async \{[\s\S]*?if \(_isYoutubeLink \|\| widget.lazyPlaylistUrl != null\) \{[\s\S]*?_currentTitle = newEps\[0\].name;[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}[\s\S]*?catch \(e\) \{[\s\S]*?\}[\s\S]*?if \(mounted\) setState\(\(\) => _isLoadingPlaylist = false\);[\s\S]*?\}"
    
    new_load = '''Future<void> _loadLazyPlaylist(String url) async {
    setState(() => _isLoadingPlaylist = true);
    try {
      List<String> args = ['--dump-json', '--flat-playlist', url];
      
      final prefs = await SharedPreferences.getInstance();
      final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
      if (isYtLinked) {
        final appDataDir = await getApplicationSupportDirectory();
        final ebPath = "\\\\\youtube_webview_profile\\\\EBWebView";
        args.insert(0, 'edge:' + ebPath);
        args.insert(0, '--cookies-from-browser');
      }

      final res = await Process.run('yt-dlp', args);
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
                m3u8Url: 'https://www.youtube.com/watch?v=' + id,
                embedUrl: 'https://i.ytimg.com/vi/' + id + '/maxresdefault.jpg'
              ));
            }
          } catch(e) {}
        }
        if (mounted && newEps.isNotEmpty) {
          setState(() {
            _episodes = newEps;
            // Also update the current episode name if we were on the first dummy one
            if (_currentIndex < _episodes.length && _episodes[_currentIndex].name.contains('loading')) {
               _episodes[_currentIndex] = Episode(
                 name: newEps[0].name,
                 slug: _episodes[_currentIndex].slug,
                 m3u8Url: _episodes[_currentIndex].m3u8Url,
                 embedUrl: _episodes[_currentIndex].embedUrl,
                 filename: _episodes[_currentIndex].filename,
               );
               if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {
                 _currentTitle = newEps[0].name;
               }
            }
          });
        }
      }
    } catch (e) {
      debugPrint('Playlist load error: \');
    }
    if (mounted) setState(() => _isLoadingPlaylist = false);
  }'''
    
    content = re.sub(old_load, new_load, content, flags=re.MULTILINE)

    # 2. Add Thumbnails
    old_child_text = r"child: Text\(\s*ep\.name,\s*style: TextStyle\(\s*color: isCurrent\s*\?\s*Colors\.blueAccent\s*:\s*Colors\.white,\s*fontWeight: isCurrent\s*\?\s*FontWeight\.bold\s*:\s*FontWeight\.normal,\s*\),\s*\),"
    
    new_child = '''child: Row(
                                            children: [
                                              if (ep.embedUrl.startsWith('https://i.ytimg.com/')) ...[
                                                ClipRRect(
                                                  borderRadius: BorderRadius.circular(6),
                                                  child: Image.network(
                                                    ep.embedUrl,
                                                    width: 100,
                                                    height: 56,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (context, error, stackTrace) => const SizedBox(width: 100, height: 56, child: Icon(Icons.error, color: Colors.white30)),
                                                  ),
                                                ),
                                                const SizedBox(width: 12),
                                              ],
                                              Expanded(
                                                child: Text(
                                                  ep.name,
                                                  style: TextStyle(
                                                    color: isCurrent
                                                        ? Colors.blueAccent
                                                        : Colors.white,
                                                    fontWeight: isCurrent
                                                        ? FontWeight.bold
                                                        : FontWeight.normal,
                                                    height: 1.3,
                                                  ),
                                                  maxLines: 2,
                                                  overflow: TextOverflow.ellipsis,
                                                ),
                                              ),
                                            ],
                                          ),'''
                                          
    content = re.sub(old_child_text, new_child, content, flags=re.MULTILINE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_all('lib/screens/player_screen.dart')
print("Fixed everything")
