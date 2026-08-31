import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add json and io imports if missing
if "dart:convert" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'dart:convert';")

# 2. Add _fetchYtQualities
fetch_func = """  Future<void> _fetchYtQualities(String url) async {
    try {
      final exeDir = File(Platform.resolvedExecutable).parent.path;
      File ytExe = File('$exeDir\\\\yt-dlp.exe');
      if (!ytExe.existsSync()) {
        ytExe = File('${Directory.current.path}\\\\build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe');
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
  }"""

if "_fetchYtQualities(" not in content:
    idx = content.find("void _changeYtQuality")
    content = content[:idx] + fetch_func + "\n\n  " + content[idx:]

# 3. Modify _ytQualities declaration
old_decl = "final List<int> _ytQualities = [0, 4320, 2160, 1440, 1080, 720, 480, 360, 240, 144];"
new_decl = "List<int> _ytQualities = [0];"
if old_decl in content:
    content = content.replace(old_decl, new_decl)

# 4. Modify _initEpisode to reset and fetch
search_init = """    setState(() {
      _currentIndex = index;
      errorMsg = null;
      _currentFallbackDomainIndex = 0; // Reset fallback domain
      _isLoadingServers = false;
      _openSubtitles = []; // clear old subs
      _selectedSubtitleTrack = null;
    });"""

new_init = search_init.replace("_selectedSubtitleTrack = null;", "_selectedSubtitleTrack = null;\n      _selectedYtHeight = 0;\n      _ytQualities = [0];")
if search_init in content:
    content = content.replace(search_init, new_init)

search_open = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
new_open = """player.open(Media(_currentUrl, httpHeaders: headers), play: false);
      if (_isYoutube) {
        _fetchYtQualities(_currentUrl);
      }"""
if search_open in content:
    content = content.replace(search_open, new_open)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched player_screen.dart")
