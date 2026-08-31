import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title in Scraper
search_scraper = """                  widget.episodes.add(Episode(
                    name: item['title'],
                    slug: item['id'],
                    m3u8Url: 'https://www.youtube.com/watch?v=' + item['id'],
                    embedUrl: 'https://i.ytimg.com/vi/' + item['id'] + '/maxresdefault.jpg'
                  ));
                  if (item['id'] == currentId) newIndex = j;
                }
                _currentIndex = newIndex;"""
new_scraper = """                  widget.episodes.add(Episode(
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
                _currentTitle = '${widget.movieName} - $epName';"""
content = content.replace(search_scraper, new_scraper)

# 2. Add Timer and Repeat State
search_state = """  bool _autoNext = true;
  double _playbackSpeed = 1.0;
  final FocusNode _focusNode = FocusNode();
  Timer? _saveProgressTimer;"""
new_state = """  bool _autoNext = true;
  double _playbackSpeed = 1.0;
  final FocusNode _focusNode = FocusNode();
  Timer? _saveProgressTimer;
  int _repeatMode = 0; // 0: off, 1: repeat all, 2: repeat one
  int _sleepTimerMinutes = 0;
  Timer? _sleepTimer;
  
  @override
  void dispose() {
    _sleepTimer?.cancel();"""
content = content.replace(search_state, new_state).replace("  @override\n  void dispose() {", "  @override\n  void dispose() {\n    _sleepTimer?.cancel();")

# 3. Add Sleep Timer Method and Modify _playNextEpisode
search_next = """  void _playNextEpisode() {
    if (_currentIndex + 1 < widget.episodes.length) {
      _initEpisode(_currentIndex + 1);
    }
  }"""
new_next = """  void _showSleepTimerDialog() {
    final TextEditingController _tc = TextEditingController(text: _sleepTimerMinutes > 0 ? _sleepTimerMinutes.toString() : '');
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: Colors.grey[900],
        title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white)),
        content: TextField(
          controller: _tc,
          keyboardType: TextInputType.number,
          style: const TextStyle(color: Colors.white),
          decoration: InputDecoration(
            hintText: 'Nhập số phút...',
            hintStyle: TextStyle(color: Colors.white54),
            enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
            focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.blueAccent)),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              setState(() {
                _sleepTimerMinutes = 0;
                _sleepTimer?.cancel();
              });
              Navigator.pop(ctx);
            },
            child: Text(L10n.t('turn_off') ?? 'Tắt', style: const TextStyle(color: Colors.redAccent)),
          ),
          TextButton(
            onPressed: () {
              final val = int.tryParse(_tc.text) ?? 0;
              setState(() {
                _sleepTimerMinutes = val;
                _sleepTimer?.cancel();
                if (val > 0) {
                  _sleepTimer = Timer(Duration(minutes: val), () {
                    if (mounted) {
                      player.pause();
                      Navigator.pop(context); // Thoát trình phát
                    }
                  });
                }
              });
              Navigator.pop(ctx);
            },
            child: Text(L10n.t('save') ?? 'Lưu', style: const TextStyle(color: Colors.blueAccent)),
          ),
        ],
      ),
    );
  }

  void _playNextEpisode() {
    if (_repeatMode == 2) {
      _initEpisode(_currentIndex);
    } else if (_currentIndex + 1 < widget.episodes.length) {
      _initEpisode(_currentIndex + 1);
    } else if (_repeatMode == 1 && widget.episodes.isNotEmpty) {
      _initEpisode(0);
    }
  }"""
content = content.replace(search_next, new_next)

# 4. Modify Format String (yt-dlp)
search_format = """    final formatStr = height == 0
        ? 'bestvideo+bestaudio/best'
        : 'bestvideo[height<=$height]+bestaudio/best';"""
new_format = """    // Ưu tiên VP9 (phần cứng hỗ trợ tốt hơn) thay vì AV1
    final formatStr = height == 0
        ? 'bestvideo[vcodec!*=av01]+bestaudio/bestvideo+bestaudio/best'
        : 'bestvideo[vcodec!*=av01][height<=$height]+bestaudio/bestvideo[height<=$height]+bestaudio/best';"""
content = content.replace(search_format, new_format)

# 5. Add Buttons to UI
search_ui = """                                              // Next Episode Button (Right side)
                                              IconButton("""
new_ui = """                                              // Repeat
                                              IconButton(
                                                icon: Icon(
                                                  _repeatMode == 2 ? Icons.repeat_one : Icons.repeat,
                                                  color: _repeatMode > 0 ? Colors.blueAccent : Colors.white,
                                                  size: 20,
                                                ),
                                                onPressed: () {
                                                  setState(() {
                                                    _repeatMode = (_repeatMode + 1) % 3;
                                                  });
                                                },
                                                tooltip: 'Lặp lại',
                                                padding: const EdgeInsets.all(4),
                                                constraints: const BoxConstraints(),
                                              ),
                                              const SizedBox(width: 8),
                                              // Sleep Timer
                                              IconButton(
                                                icon: Icon(
                                                  Icons.timer,
                                                  color: _sleepTimerMinutes > 0 ? Colors.blueAccent : Colors.white,
                                                  size: 20,
                                                ),
                                                onPressed: _showSleepTimerDialog,
                                                tooltip: _sleepTimerMinutes > 0 ? 'Hẹn giờ: $_sleepTimerMinutes phút' : 'Hẹn giờ tắt',
                                                padding: const EdgeInsets.all(4),
                                                constraints: const BoxConstraints(),
                                              ),
                                              const SizedBox(width: 8),
                                              // Next Episode Button (Right side)
                                              IconButton("""
content = content.replace(search_ui, new_ui)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen features.")
