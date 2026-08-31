import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports
if "import 'dart:convert';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'dart:convert';\nimport 'dart:io';\nimport 'dart:async';\nimport 'package:shared_preferences/shared_preferences.dart';\nimport 'package:cached_network_image/cached_network_image.dart';")

# 2. State vars
var_search = "bool _isPlaying = false;"
var_inject = """bool _isPlaying = false;
  int _selectedYtHeight = 0;
  List<int> _ytQualities = [0];
  bool _isRepeat = false;
  int _sleepTimerMinutes = 0;
  Timer? _sleepTimer;
  DateTime? _sleepEndTime;"""
if "int _selectedYtHeight = 0;" not in content:
    content = content.replace(var_search, var_inject)

# 3. _isYoutube and fetch and start timer
func_inject = """  bool get _isYoutube {
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

  Future<void> _fetchYtQualities(String url) async {
    try {
      final exeDir = File(Platform.resolvedExecutable).parent.path;
      File ytExe = File('$exeDir\\\\yt-dlp.exe');
      if (!ytExe.existsSync()) {
        ytExe = File('${Directory.current.path}\\\\build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe');
      }
      final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';
      
      final prefs = await SharedPreferences.getInstance();
      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      List<String> args = ['-J', url];
      if (cookieSource != 'none') {
        args.insert(0, cookieSource);
        args.insert(0, '--cookies-from-browser');
      }
      
      final res = await Process.run(exePath, args);
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

  void _startSleepTimer() {
    _sleepTimer?.cancel();
    if (_sleepTimerMinutes > 0) {
      _sleepEndTime = DateTime.now().add(Duration(minutes: _sleepTimerMinutes));
      _sleepTimer = Timer(Duration(minutes: _sleepTimerMinutes), () {
        if (mounted) {
          player.pause();
          setState(() {
            _sleepTimerMinutes = 0;
            _sleepEndTime = null;
          });
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Đã đến giờ hẹn. Đã tạm dừng phát nhạc.')),
          );
        }
      });
    } else {
      _sleepEndTime = null;
    }
  }

  void _setPlaybackSpeed"""
if "Future<void> _fetchYtQualities" not in content:
    content = content.replace("void _setPlaybackSpeed", func_inject)

# 4. _initEpisode
search_init = """_selectedSubtitleTrack = null;
    });"""
new_init = search_init.replace("_selectedSubtitleTrack = null;", "_selectedSubtitleTrack = null;\n      _selectedYtHeight = 0;\n      _ytQualities = [0];")
if "_selectedYtHeight = 0;" not in content:
    content = content.replace(search_init, new_init)

search_open = """player.open(Media(_currentUrl, httpHeaders: headers), play: false);"""
new_open = """
      final prefs = await SharedPreferences.getInstance();
      _isRepeat = prefs.getBool('default_repeat') ?? false;
      _sleepTimerMinutes = prefs.getInt('default_sleep_timer') ?? 0;
      _startSleepTimer();
      player.setPlaylistMode(_isRepeat ? PlaylistMode.single : PlaylistMode.none);

      final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
      if (cookieSource != 'none' && _isYoutube) {
        (player.platform as dynamic).setProperty('ytdl-raw-options', 'cookies-from-browser=$cookieSource');
      } else {
        (player.platform as dynamic).setProperty('ytdl-raw-options', '');
      }
      
      player.open(Media(_currentUrl, httpHeaders: headers), play: false);
      if (_isYoutube) {
        _fetchYtQualities(_currentUrl);
      }"""
if "_fetchYtQualities(_currentUrl);" not in content:
    content = content.replace(search_open, new_open)

# 5. UI Qualities
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
                                          child: Text(h == 0 ? 'Tự động (Cao nhất)' : '${h}p${h == 4320 ? ' (8K)' : h == 2160 ? ' (4K)' : h == 1440 ? ' (2K)' : ''}'),
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
if "if (_isYoutube) ...[" not in content:
    content = content.replace(search_ui, new_ui)

# 6. Audio Background Cover
search_bg = """          return Center(
            child: Icon(Icons.music_note, color: Colors.white.withOpacity(0.5), size: 100),
          );"""
new_bg = """          final ep = widget.episodes[_currentIndex];
          if (ep.embedUrl.isNotEmpty && ep.embedUrl.startsWith('http')) {
            return Positioned.fill(
              child: CachedNetworkImage(
                imageUrl: ep.embedUrl,
                fit: BoxFit.cover,
                color: Colors.black.withOpacity(0.5),
                colorBlendMode: BlendMode.darken,
              ),
            );
          }
          return Center(
            child: Icon(Icons.music_note, color: Colors.white.withOpacity(0.5), size: 100),
          );"""
if "CachedNetworkImage(" not in content:
    content = content.replace(search_bg, new_bg)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart")
