import re

def patch_real_youtube_qualities(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the hardcoded list to an empty list
    content = content.replace(
        "final List<String> _ytQualities = ['8K (4320p)', '4K (2160p)', '1440p', '1080p', '720p', '480p'];",
        "List<String> _ytQualities = [];"
    )

    # 2. Add the _fetchYoutubeQualities method
    fetch_method = '''
  Future<void> _fetchYoutubeQualities(String url) async {
    try {
      final result = await Process.run('yt-dlp', ['-J', '--no-warnings', url]);
      if (result.exitCode == 0) {
        final data = jsonDecode(result.stdout);
        final formats = data['formats'] as List;
        final Set<int> heights = {};
        for (var f in formats) {
          if (f['vcodec'] != 'none' && f['vcodec'] != null && f['height'] != null) {
            heights.add(f['height'] as int);
          }
        }
        final sorted = heights.toList()..sort((a, b) => b.compareTo(a));
        final List<String> realQualities = [];
        for (var h in sorted) {
          if (h >= 4320) realQualities.add('8K (4320p)');
          else if (h >= 2160) realQualities.add('4K (2160p)');
          else if (h == 1440) realQualities.add('1440p');
          else if (h == 1080) realQualities.add('1080p');
          else if (h == 720) realQualities.add('720p');
          else if (h == 480) realQualities.add('480p');
          else if (h == 360) realQualities.add('360p');
          else if (h == 240) realQualities.add('240p');
          else if (h == 144) realQualities.add('144p');
        }
        if (mounted) {
          setState(() {
            _ytQualities = realQualities.toSet().toList();
            if (!_ytQualities.contains(_selectedYtQuality) && _ytQualities.isNotEmpty) {
              // Try to find the closest fallback or just pick highest
              bool found = false;
              if (_selectedYtQuality.contains('4K') && _ytQualities.contains('1080p')) {
                 _selectedYtQuality = '1080p'; found = true;
              }
              if (!found) _selectedYtQuality = _ytQualities.first;
            }
          });
        }
      }
    } catch (e) {
      debugPrint('yt-dlp parse error: \');
    }
  }
'''
    # We will inject this before _initMediaKit
    content = content.replace("void _initMediaKit() {", fetch_method + "\n  void _initMediaKit() {")

    # 3. Call _fetchYoutubeQualities in _playCurrentUrl
    # Search for player.open(Media(_currentUrl, httpHeaders: headers), play: false);
    target_play = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    replacement_play = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);\n      if (_isYoutubeLink) _fetchYoutubeQualities(_currentUrl);"
    
    # Avoid duplicate injection
    if "_fetchYoutubeQualities(_currentUrl);" not in content:
        content = content.replace(target_play, replacement_play)

    # 4. Make sure dart:convert is imported for jsonDecode
    if "import 'dart:convert';" not in content:
        content = content.replace("import 'dart:async';", "import 'dart:async';\nimport 'dart:convert';")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_real_youtube_qualities('lib/screens/player_screen.dart')
print("Patched Real YouTube Qualities via yt-dlp JSON")
