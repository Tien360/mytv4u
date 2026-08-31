import re

def patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_load = r"Future<void> _loadLazyPlaylist\(String url\) async \{[\s\S]*?if \(_isYoutubeLink \|\| widget.lazyPlaylistUrl != null\) \{[\s\S]*?_currentTitle = newEps\[0\].name;[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}[\s\S]*?catch \(e\) \{[\s\S]*?\}[\s\S]*?if \(mounted\) setState\(\(\) => _isLoadingPlaylist = false\);[\s\S]*?\}"

    new_load = '''Future<void> _loadLazyPlaylist(String url) async {
    setState(() => _isLoadingPlaylist = true);
    try {
      final exeDir = File(Platform.resolvedExecutable).parent.path;
      File ytExe = File('\\\\\yt-dlp.exe');
      if (!ytExe.existsSync()) {
        ytExe = File('\\\\\build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe');
      }
      final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';

      List<String> args = ['--dump-json', '--flat-playlist', url];
      final prefs = await SharedPreferences.getInstance();
      final isYtLinked = prefs.getBool('is_yt_linked') ?? false;
      if (isYtLinked) {
        final appDataDir = await getApplicationSupportDirectory();
        final ebPath = appDataDir.path + '\\\\youtube_webview_profile\\\\EBWebView';
        args.insert(0, 'edge:' + ebPath);
        args.insert(0, '--cookies-from-browser');
      }

      ProcessResult res = await Process.run(exePath, args);
      
      // FALLBACK if cookie extraction fails
      if (res.exitCode != 0 && isYtLinked) {
        debugPrint('Cookie extraction failed. Retrying without cookies...');
        res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
      }

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
      } else {
         debugPrint('yt-dlp failed: \');
      }
    } catch (e) {
      debugPrint('Playlist load error: \');
    }
    if (mounted) setState(() => _isLoadingPlaylist = false);
  }'''
  
    match = re.search(old_load, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_load)
    else:
        print("Could not find _loadLazyPlaylist")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch('lib/screens/player_screen.dart')
print("Patched loadLazyPlaylist")
