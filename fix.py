import io
import re

with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Icons.color_lens' in line:
        lines[i+1] = "                                  title: const Text('Bộ lọc màu Video', style: TextStyle(color: Colors.white)),\n"
    if 'Icons.av_timer' in line and 'thanh' in lines[i+1]:
        lines[i+1] = "                                  title: const Text('Đồng bộ Âm thanh', style: TextStyle(color: Colors.white)),\n"
    if 'Icons.av_timer' in line and 'Ph' in lines[i+1]:
        lines[i+1] = "                                  title: const Text('Đồng bộ Phụ đề', style: TextStyle(color: Colors.white)),\n"

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done!')
