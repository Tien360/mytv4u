import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State variable
if "int _selectedYtHeight = 0;" not in content:
    content = content.replace("bool _isPlaying = false;", "bool _isPlaying = false;\n  int _selectedYtHeight = 0;\n  final List<int> _ytQualities = [0, 4320, 2160, 1440, 1080, 720, 480, 360, 240, 144];")

# 2. Add _isYoutube getter
if "bool get _isYoutube" not in content:
    content = content.replace("void _setPlaybackSpeed(double speed) {", """bool get _isYoutube {
    if (_currentUrl.isEmpty) return false;
    return _currentUrl.contains('youtube.com') || _currentUrl.contains('youtu.be') || widget.episodes[_currentIndex].slug.startsWith('yt_');
  }

  void _changeYtQuality(int height) async {
    setState(() => _selectedYtHeight = height);
    final formatStr = height == 0
        ? 'bestvideo+bestaudio/best'
        : 'bestvideo[height<=$height]+bestaudio/best';
    try {
      (player.platform as dynamic).setProperty('ytdl-format', formatStr);
    } catch (_) {}

    final pos = player.state.position;
    await player.open(Media(_currentUrl));
    if (pos > Duration.zero) {
      await player.seek(pos);
    }
  }

  void _setPlaybackSpeed(double speed) {""")

# 3. Add UI inside "Chất lượng video" section
search_ui = """                                if (_videoTracks.isNotEmpty) ...["""
new_ui = """                                if (_isYoutube) ...[
                                  ListTile(
                                    title: Text(L10n.t('video_quality') ?? 'Chất lượng video', style: const TextStyle(color: Colors.white)),
                                    trailing: DropdownButton<int>(
                                      dropdownColor: Colors.grey[900],
                                      value: _selectedYtHeight,
                                      style: const TextStyle(color: Colors.blueAccent),
                                      items: _ytQualities.map((h) {
                                        return DropdownMenuItem<int>(
                                          value: h,
                                          child: Text(h == 0 ? 'Tự động (Chất lượng cao nhất)' : '${h}p${h == 4320 ? ' (8K)' : h == 2160 ? ' (4K)' : h == 1440 ? ' (2K)' : ''}'),
                                        );
                                      }).toList(),
                                      onChanged: (val) {
                                        if (val != null) {
                                          _changeYtQuality(val);
                                          setTabState(() {});
                                        }
                                      },
                                    ),
                                  ),
                                  const Divider(color: Colors.white24),
                                ] else if (_videoTracks.isNotEmpty) ...["""

if search_ui in content:
    content = content.replace(search_ui, new_ui)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched player_screen.dart successfully")
else:
    print("Could not find search_ui")

