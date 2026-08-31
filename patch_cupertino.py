import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add cupertino import
if "package:flutter/cupertino.dart" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:flutter/cupertino.dart';")

# 2. Add _formatSleepTimer method somewhere inside the State class
if "String _formatSleepTimer" not in content:
    format_method = """  String _formatSleepTimer(int seconds) {
    int h = seconds ~/ 3600;
    int m = (seconds % 3600) ~/ 60;
    int s = seconds % 60;
    if (h > 0) {
      return '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
    }
    return '${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
  }\n\n"""
    # put it right before _showSleepTimerDialog
    content = content.replace("  void _showSleepTimerDialog() {", format_method + "  void _showSleepTimerDialog() {")

# 3. Replace state variables and cancel call in dispose
content = content.replace("int _sleepTimerMinutes = 0;", "int _sleepSecondsRemaining = 0;")
# We also have to be careful with other _sleepTimerMinutes occurences, let's just replace the whole methods block

# 4. Replace the methods
start_str = "  void _showSleepTimerDialog() {"
end_str = "  void _playNextEpisode() {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

new_methods = """  void _showSleepTimerDialog() {
    showCupertinoModalPopup(
      context: context,
      builder: (BuildContext context) => CupertinoTheme(
        data: const CupertinoThemeData(brightness: Brightness.dark),
        child: CupertinoActionSheet(
          title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tự động tắt', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          message: const Text('Chọn khoảng thời gian để tự động dừng phát và thoát.'),
          actions: <CupertinoActionSheetAction>[
            CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(context);
                _setSleepTimer(60);
              },
              child: const Text('60 phút', style: TextStyle(color: Colors.blueAccent)),
            ),
            CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(context);
                _setSleepTimer(120);
              },
              child: const Text('120 phút', style: TextStyle(color: Colors.blueAccent)),
            ),
            CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(context);
                _setSleepTimer(180);
              },
              child: const Text('180 phút', style: TextStyle(color: Colors.blueAccent)),
            ),
            CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(context);
                _showCustomSleepTimerDialog();
              },
              child: const Text('Tùy chỉnh...', style: TextStyle(color: Colors.orange)),
            ),
          ],
          cancelButton: CupertinoActionSheetAction(
            isDestructiveAction: true,
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _sleepSecondsRemaining = 0;
                _sleepTimer?.cancel();
              });
            },
            child: Text(L10n.t('turn_off') ?? 'Tắt hẹn giờ'),
          ),
        ),
      ),
    );
  }

  void _showCustomSleepTimerDialog() {
    Duration initialTimer = Duration(seconds: _sleepSecondsRemaining > 0 ? _sleepSecondsRemaining : 0);
    Duration selectedDuration = initialTimer;
    
    showCupertinoModalPopup(
      context: context,
      builder: (BuildContext builder) {
        return Container(
          height: 320.0,
          color: const Color(0xFF1C1C1E),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  CupertinoButton(
                    child: const Text('Hủy', style: TextStyle(color: Colors.redAccent)),
                    onPressed: () => Navigator.pop(context),
                  ),
                  CupertinoButton(
                    child: const Text('Đồng ý', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                    onPressed: () {
                      Navigator.pop(context);
                      if (selectedDuration.inMinutes > 0) {
                        _setSleepTimer(selectedDuration.inMinutes);
                      }
                    },
                  ),
                ],
              ),
              Expanded(
                child: SafeArea(
                  top: false,
                  child: CupertinoTheme(
                    data: const CupertinoThemeData(brightness: Brightness.dark),
                    child: CupertinoTimerPicker(
                      mode: CupertinoTimerPickerMode.hm,
                      initialTimerDuration: initialTimer,
                      onTimerDurationChanged: (Duration newDuration) {
                        selectedDuration = newDuration;
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _setSleepTimer(int minutes) {
    if (minutes <= 0) return;
    setState(() {
      _sleepSecondsRemaining = minutes * 60;
      _sleepTimer?.cancel();
      _sleepTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
        if (!mounted) {
          timer.cancel();
          return;
        }
        setState(() {
          if (_sleepSecondsRemaining > 0) {
            _sleepSecondsRemaining--;
          }
          if (_sleepSecondsRemaining <= 0) {
            timer.cancel();
            player.pause();
            Navigator.pop(context);
          }
        });
      });
    });
  }

"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_methods + content[end_idx:]

# 5. Fix the ListTile. Because of CP1252 parsing, let's use regex matching carefully.
old_tile_pattern = r"ListTile\(\s*leading:\s*Icon\(Icons\.timer,\s*color:\s*_sleepTimerMinutes.*?\),\s*title:\s*const\s*Text\('.*?',\s*style:\s*TextStyle\(color:\s*Colors\.white\)\),\s*subtitle:\s*Text\(.*?\),\s*trailing:\s*const\s*Icon\(Icons\.chevron_right,\s*color:\s*Colors\.white54\),\s*onTap:\s*\(\)\s*\{\s*Navigator\.pop\(context\);\s*_showSleepTimerDialog\(\);\s*\},\s*\),"
new_tile = """ListTile(
                                  leading: Icon(Icons.timer, color: _sleepSecondsRemaining > 0 ? Colors.blueAccent : Colors.white),
                                  title: const Text('Hẹn giờ tắt', style: TextStyle(color: Colors.white)),
                                  subtitle: Text(_sleepSecondsRemaining > 0 ? 'Còn lại ${_formatSleepTimer(_sleepSecondsRemaining)}' : 'Đang tắt', style: const TextStyle(color: Colors.white54)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    _showSleepTimerDialog();
                                  },
                                ),"""

content = re.sub(old_tile_pattern, new_tile, content, flags=re.DOTALL)

# Let's fallback if regex missed because of encoding (it should work if we dotall everything)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished patching cupertino UI")
