import io
import re

with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Just replace by finding the icon
c = re.sub(r'Icon\(Icons\.color_lens.*?\)\,\n.*?title.*?Text\([^)]+\)', \"Icon(Icons.color_lens, color: Colors.blueAccent),\\n                                  title: const Text('Bộ lọc màu Video', style: TextStyle(color: Colors.white))\", c)
c = re.sub(r'Icon\(Icons\.av_timer.*?\)\,\n.*?title.*?Text\(.*?Ä á»“ng bá»™.*?thanh.*?\)', \"Icon(Icons.av_timer, color: Colors.blueAccent),\\n                                  title: const Text('Đồng bộ Audio', style: TextStyle(color: Colors.white))\", c)
c = re.sub(r'Icon\(Icons\.av_timer.*?\)\,\n.*?title.*?Text\(.*?Ä á»“ng bá»™.*?Phá»¥ Ä‘á» .*?\)', \"Icon(Icons.av_timer, color: Colors.blueAccent),\\n                                  title: const Text('Đồng bộ Phụ đề', style: TextStyle(color: Colors.white))\", c)

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed encodings')
