import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add _ytQualities state
search_state = """  bool _autoNext = true;"""
new_state = """  bool _autoNext = true;
  List<int> _ytQualities = [0];
  int _selectedYtHeight = 0;
  bool _isYoutube = false;"""
if "_ytQualities =" not in content:
    content = content.replace(search_state, new_state)

# Add _fetchYtQualities and _changeYtQuality methods
new_methods = """
  Future<void> _fetchYtQualities(String url) async {
    try {
      final exeDir = File(Platform.resolvedExecutable).parent.path;
      File ytExe = File('$exeDir\\yt-dlp.exe');
      if (!ytExe.existsSync()) {
        ytExe = File('${Directory.current.path}\\build\\windows\\x64\\runner\\Release\\yt-dlp.exe');
      }
      final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';
      
      final res = await Process.run(exePath, ['-J', url]);
      if (res.exitCode == 0) {
        final json = jsonDecode(res.stdout);
        final formats = json['formats'] as List?;
        if (formats != null) {
          final Set<int> heights = {};
          for (var f in formats) {
            if (f['vcodec'] != 'none' && f['height'] != null) {
              heights.add(f['height'] as int);
            }
          }
          if (mounted && heights.isNotEmpty) {
            final sorted = heights.toList()..sort((a, b) => b.compareTo(a));
            setState(() {
              _ytQualities = [0, ...sorted];
            });
          }
        }
      }
    } catch (e) {
      print('Fetch YT qualities error: $e');
    }
  }

  void _changeYtQuality(int height) async {
    setState(() => _selectedYtHeight = height);
    final formatStr = height == 0
        ? 'bestvideo[vcodec!*=av01]+bestaudio/bestvideo+bestaudio/best'
        : 'bestvideo[vcodec!*=av01][height<=$height]+bestaudio/bestvideo[height<=$height]+bestaudio/best';
    try {
      (player.platform as dynamic).setProperty('ytdl-format', formatStr);
    } catch (_) {}

    final pos = player.state.position;
    await player.open(Media(_currentUrl));
    if (pos > Duration.zero) {
      await player.seek(pos);
    }
  }
"""
if "_fetchYtQualities" not in content:
    content = content.replace("  void _setPlaybackSpeed(double speed)", new_methods + "\n  void _setPlaybackSpeed(double speed)")

# Add _isYoutube check in _playCurrentUrl
search_play = """      player.open(Media(_currentUrl, httpHeaders: headers), play: false);"""
new_play = """      player.open(Media(_currentUrl, httpHeaders: headers), play: false);
      _isYoutube = _currentUrl.contains('youtube.com') || _currentUrl.contains('youtu.be');
      if (_isYoutube) {
        _ytQualities = [0];
        _selectedYtHeight = 0;
        _fetchYtQualities(_currentUrl);
      }"""
if "_isYoutube = _currentUrl.contains" not in content:
    content = content.replace(search_play, new_play)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Step 1 done")
