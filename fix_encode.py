import io
import re

with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'Bá»™ lá» c mÃ.u Video', 'Bộ lọc màu Video', c)
c = re.sub(r'Ä á»“ng bá»™ trÃª áº¢m thanh', 'Đồng bộ Audio', c)
c = re.sub(r'Ä á»“ng bá»™ trÃª Phá»¥ Ä‘á» ', 'Đồng bộ Phụ đề', c)

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed encodings')
