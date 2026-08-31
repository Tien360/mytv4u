import re

path1 = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path1, 'r', encoding='utf-8') as f:
    content1 = f.read()

# Fix settings_screen.dart variables
bad_str = """  bool _backgroundPlayback = false;
                  _defaultRepeat = false;
                  _defaultSleepTimer = 0;
  bool _defaultRepeat = false;
  int _defaultSleepTimer = 0;"""
good_str = """  bool _backgroundPlayback = false;
  bool _defaultRepeat = false;
  int _defaultSleepTimer = 0;"""
content1 = content1.replace(bad_str, good_str)
with open(path1, 'w', encoding='utf-8') as f:
    f.write(content1)


path2 = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path2, 'r', encoding='utf-8') as f:
    content2 = f.read()

# Fix player_screen.dart state variables
if "bool _isRepeat = false;" not in content2:
    content2 = content2.replace("bool _isPlaying = false;", "bool _isPlaying = false;\n  bool _isRepeat = false;\n  int _sleepTimerMinutes = 0;\n  Timer? _sleepTimer;\n  DateTime? _sleepEndTime;")
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(content2)

print("Fixed settings and player!")
