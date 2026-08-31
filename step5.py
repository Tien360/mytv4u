import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search_ui = """                                              // Next Episode Button (Right side)
                                              IconButton(
                                                icon: const Icon(
                                                  Icons.skip_next,"""
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
                                              IconButton(
                                                icon: const Icon(
                                                  Icons.skip_next,"""
content = content.replace(search_ui, new_ui)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Step 5 done")
