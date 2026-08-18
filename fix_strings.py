import io

with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Bá»™ lá» c mÃ u Video", "Bộ lọc màu Video")
content = content.replace("Ä á»“ng bá»™ trÃª áº¢m thanh", "Đồng bộ trễ Âm thanh")
content = content.replace("Ä á»“ng bá»™ trÃª Phá»¥ Ä‘á» ", "Đồng bộ trễ Phụ đề")

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed strings')
