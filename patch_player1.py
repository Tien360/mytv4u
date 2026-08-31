import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State vars
if "bool _isRepeat = false;" not in content:
    content = content.replace("bool _isPlaying = true;", "bool _isPlaying = true;\n  bool _isRepeat = false;\n  int _sleepTimerMinutes = 0;\n  Timer? _sleepTimer;\n  DateTime? _sleepEndTime;")

# 2. cancel timer in dispose
if "_sleepTimer?.cancel();" not in content:
    content = content.replace("player.dispose();", "_sleepTimer?.cancel();\n    player.dispose();")

# 3. add timer logic
timer_logic = """  void _startSleepTimer(int minutes) {
    _sleepTimer?.cancel();
    if (minutes <= 0) {
      setState(() {
        _sleepTimerMinutes = 0;
        _sleepEndTime = null;
      });
      return;
    }
    setState(() {
      _sleepTimerMinutes = minutes;
      _sleepEndTime = DateTime.now().add(Duration(minutes: minutes));
    });
    _sleepTimer = Timer(Duration(minutes: minutes), () {
      if (mounted) {
        player.pause();
        setState(() {
          _sleepTimerMinutes = 0;
          _sleepEndTime = null;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Đã hết thời gian hẹn giờ ngủ. Trình phát đã tạm dừng.', style: TextStyle(color: Colors.white)), backgroundColor: Colors.black87),
        );
      }
    });
  }
"""
if "_startSleepTimer" not in content:
    # insert before _loadSettingsAndInit
    content = content.replace("Future<void> _loadSettingsAndInit() async {", timer_logic + "\n  Future<void> _loadSettingsAndInit() async {")

# 4. load in _loadSettingsAndInit
if "default_repeat" not in content:
    content = content.replace("_backgroundPlayback = prefs.getBool('background_playback') ?? false;", "_backgroundPlayback = prefs.getBool('background_playback') ?? false;\n      _isRepeat = prefs.getBool('default_repeat') ?? false;\n      _sleepTimerMinutes = prefs.getInt('default_sleep_timer') ?? 0;")
    
    # After player initialization (around _initEpisode or inside _loadSettingsAndInit), we should apply these
    # Actually wait, _loadSettingsAndInit runs before _initEpisode? Yes.
    # We can just apply it directly after reading.
    apply_logic = """      if (_isRepeat) {
        player.setPlaylistMode(PlaylistMode.single);
      }
      if (_sleepTimerMinutes > 0) {
        _startSleepTimer(_sleepTimerMinutes);
      }
"""
    content = content.replace("_sleepTimerMinutes = prefs.getInt('default_sleep_timer') ?? 0;", "_sleepTimerMinutes = prefs.getInt('default_sleep_timer') ?? 0;\n" + apply_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched player_screen.dart State and Logic")
