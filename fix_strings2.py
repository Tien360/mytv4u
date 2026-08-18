import io
import codecs

with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the literal corrupted string and replace it.
content = content.replace('Bá»™ lá» c mÃ\xa0u Video', 'Bộ lọc màu Video')
content = content.replace('Ä\x91á»\x93ng bá»™ trÃª áº¢m thanh', 'Đồng bộ trễ Âm thanh')
content = content.replace('Ä\x91á»\x93ng bá»™ trÃª Phá»¥ Ä\x91á»\x9d', 'Đồng bộ trễ Phụ đề')
content = content.replace('Ä\x90á»\x93ng bá»™ trÃª áº¢m thanh', 'Đồng bộ trễ Âm thanh')
content = content.replace('Ä\x90á»\x93ng bá»™ trÃª Phá»¥ Ä\x91á»\x9d', 'Đồng bộ trễ Phụ đề')

# Also handle the copy-pasted string in patch_player2.py: 'Ä á»“ng bá»™ trÃª áº¢m thanh' etc.
content = content.replace('Ä á»“ng bá»™ trÃª áº¢m thanh', 'Đồng bộ trễ Âm thanh')
content = content.replace('Ä á»“ng bá»™ trÃª Phá»¥ Ä‘á» ', 'Đồng bộ trễ Phụ đề')

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed strings')
