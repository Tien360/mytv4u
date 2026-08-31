import re

def patch_youtube_quality(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove 4K texture cap
    content = content.replace("width: 3840, height: 2160, \n        ", "")

    # 2. Add state for YouTube quality
    state_injection = '''
  // YouTube Quality State
  final List<String> _ytQualities = ['8K (4320p)', '4K (2160p)', '1440p', '1080p', '720p', '480p'];
  String _selectedYtQuality = '4K (2160p)';
  
  bool get _isYoutubeLink => _currentUrl.contains('youtube.com') || _currentUrl.contains('youtu.be');
'''
    if "List<String> _ytQualities" not in content:
        content = content.replace("List<VideoTrack> _videoTracks = [];", state_injection + "  List<VideoTrack> _videoTracks = [];")

    # 3. Modify _playCurrentUrl to set ytdl-format based on _selectedYtQuality
    target_play = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    replacement_play = '''
      if (_isYoutubeLink) {
        String heightTarget = '2160';
        if (_selectedYtQuality.contains('8K')) heightTarget = '4320';
        else if (_selectedYtQuality.contains('4K')) heightTarget = '2160';
        else if (_selectedYtQuality.contains('1440p')) heightTarget = '1440';
        else if (_selectedYtQuality.contains('1080p')) heightTarget = '1080';
        else if (_selectedYtQuality.contains('720p')) heightTarget = '720';
        else if (_selectedYtQuality.contains('480p')) heightTarget = '480';
        
        try {
           player.platform?.setProperty('ytdl-format', 'bestvideo[height<=?'+heightTarget+']+bestaudio/best');
        } catch(e) {}
      }
      player.open(Media(_currentUrl, httpHeaders: headers), play: false);'''
    if "_isYoutubeLink" not in content.split("player.open(Media(_currentUrl")[0]:
        content = content.replace(target_play, replacement_play)

    # 4. Modify UI to show YouTube Quality dropdown
    target_ui = '''if (_videoTracks.isNotEmpty) ...['''
    replacement_ui = '''if (_isYoutubeLink) ...[
                                  ListTile(
                                    title: Text(
                                      L10n.t('video_quality') ?? 'Chất lượng Video',
                                      style: const TextStyle(color: Colors.white),
                                    ),
                                    trailing: DropdownButton<String>(
                                      dropdownColor: Colors.grey[900],
                                      value: _selectedYtQuality,
                                      style: const TextStyle(color: Colors.white),
                                      underline: const SizedBox(),
                                      items: _ytQualities.map((q) {
                                        return DropdownMenuItem(
                                          value: q,
                                          child: Text(q, style: const TextStyle(fontSize: 14)),
                                        );
                                      }).toList(),
                                      onChanged: (val) async {
                                        if (val != null) {
                                          setState(() => _selectedYtQuality = val);
                                          final pos = _position;
                                          await _playCurrentUrl(widget.episodes[_currentIndex]);
                                          await player.seek(pos);
                                          player.play();
                                        }
                                      },
                                    ),
                                  ),
                                ] else if (_videoTracks.isNotEmpty) ...['''
    if "if (_isYoutubeLink) ...[" not in content:
        content = content.replace(target_ui, replacement_ui)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_youtube_quality('lib/screens/player_screen.dart')
print("Patched YouTube Quality logic in player_screen")
