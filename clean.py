import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicates
search_dup = """  int _repeatMode = 0; // 0: off, 1: repeat all, 2: repeat one
  int _sleepTimerMinutes = 0;
  Timer? _sleepTimer;
  int _repeatMode = 0; // 0: off, 1: repeat all, 2: repeat one
  int _sleepTimerMinutes = 0;
  Timer? _sleepTimer;"""
new_dup = """  int _repeatMode = 0; // 0: off, 1: repeat all, 2: repeat one
  int _sleepTimerMinutes = 0;
  Timer? _sleepTimer;"""
if search_dup in content:
    content = content.replace(search_dup, new_dup)

# Fix dart:convert
if "import 'dart:convert';" not in content:
    content = content.replace("import 'dart:async';", "import 'dart:async';\nimport 'dart:convert';")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up duplicates and imports")
