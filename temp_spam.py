import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add _spamCount and _spamTimer
spam_vars = """  int _spamCount = 0;
  Timer? _spamTimer;"""

c = c.replace("  String _progressKey = 'chill';", "  String _progressKey = 'chill';\n" + spam_vars)

# 2. Modify _triggerEffect
old_trigger = """  void _triggerEffect() async {
    if (!_easterEggsEnabled || _isAnimatingText) return;
    setState(() => _isAnimatingText = true);
    final rnd = Random();
    final roll = rnd.nextInt(100);"""

new_trigger = """  void _triggerEffect() async {
    if (!_easterEggsEnabled) return;
    
    _spamCount++;
    _spamTimer?.cancel();
    _spamTimer = Timer(const Duration(seconds: 4), () {
      if (mounted) setState(() => _spamCount = 0);
    });

    setState(() => _isAnimatingText = true);
    final rnd = Random();
    
    if (_spamCount > 4) {
      await _dispatch(ScenarioGroup.spam, OutputType.toast, rnd);
      await Future.delayed(const Duration(seconds: 1));
      if (mounted) setState(() => _isAnimatingText = false);
      return;
    }
    if (_isAnimatingText && _spamCount <= 1) {
       // Allow animation reset
    }

    final roll = rnd.nextInt(100);"""

c = c.replace(old_trigger, new_trigger)

# 3. Add ScenarioGroup.spam to enum
c = c.replace("enum ScenarioGroup { universal, genre, progress, legendary }", "enum ScenarioGroup { universal, genre, progress, legendary, spam }")

# 4. Handle spam in _dispatch
old_dispatch = """      case ScenarioGroup.progress: await _progressFx(out, rnd); break;
      case ScenarioGroup.legendary: break;
    }"""
new_dispatch = """      case ScenarioGroup.progress: await _progressFx(out, rnd); break;
      case ScenarioGroup.legendary: break;
      case ScenarioGroup.spam: await _spamFx(rnd); break;
    }"""
c = c.replace(old_dispatch, new_dispatch)

# 5. Add _spamFx method
spam_fx_method = """
  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? 'Phim này';
    final spamJokes = [
      "Bấm gì bấm nhiều thế? Bộ tính làm hacker hở?",
      "Bạn có spam cháy cả chuột thì phim cũng chưa ra tập mới đâu!",
      "Thơ tặng bạn:\\n$movieName hay thật là hay\\nNhưng mà chưa chiếu, bấm hoài đứt tay!",
      "Tôi là hộp báo lịch, không phải máy đẻ tập phim mới nha!",
      "Đã bảo là chưa có mà! Lì xì admin 50k đi rồi tôi giục đạo diễn cho.",
      "Hết văn để trêu bạn rồi! Mỏi tay chưa? Tắt máy đi ngủ đi!",
      "Bạn bấm nát cái nút rồi kìa. Lạy chúa tôi!",
      "Nếu bạn bấm thêm 100 lần nữa, tập mới sẽ... vẫn không xuất hiện =))",
      "Thơ về phim:\\n$movieName kịch tính bất ngờ\\nSpam hoài đau ngón, thẫn thờ chờ mong!",
      "Nghịch hoài không chán hả bạn gì ơi?",
      "Nhấp chuột 10 lần 1 giây... bạn chơi game MOBA chắc pro lắm nhỉ?",
      "Đã bảo là không có gì đâu mà cứ bấm! Ngoan, đi xem phim khác đi."
    ];
    
    _progressKey = 'rage';
    _showToast([spamJokes[rnd.nextInt(spamJokes.length)]], rnd);
    // Vibrate text
    if (mounted) setState(() {});
  }
"""

c = c.replace("  Future<void> _universalFx", spam_fx_method + "\n  Future<void> _universalFx")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Added Spam Easter Eggs!")
