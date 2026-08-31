import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole ListTile for sleep timer
old_list_tile_pattern = r"ListTile\(\s*leading:\s*Icon\(Icons\.timer,.*?\),\s*title:\s*const\s*Text\('H.*?gi.*?t.*?t',.*?\),\s*subtitle:\s*Text\(_sleepTimerMinutes > 0 \? 'C.*?l.*?i \$_sleepTimerMinutes ph.*?t' : '.*?ang t.*?t',.*?\),\s*trailing:\s*const\s*Icon\(Icons\.chevron_right,.*?\),\s*onTap:\s*\(\)\s*\{\s*Navigator\.pop\(context\);\s*_showSleepTimerDialog\(\);\s*\},\s*\),"

new_list_tile = """ListTile(
                                  leading: Icon(Icons.timer, color: _sleepTimerMinutes > 0 ? Colors.blueAccent : Colors.white),
                                  title: const Text('Hẹn giờ tắt', style: TextStyle(color: Colors.white)),
                                  subtitle: Text(_sleepTimerMinutes > 0 ? 'Còn lại $_sleepTimerMinutes phút' : 'Đang tắt', style: const TextStyle(color: Colors.white54)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    _showSleepTimerDialog();
                                  },
                                ),"""

content = re.sub(old_list_tile_pattern, new_list_tile, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen ListTile")
