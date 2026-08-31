import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will just replace the subtitle line using a regex to be safe
pattern = r"subtitle: Text\(_sleepTimerMinutes > 0 \? '.*?\$sleepTimerMinutes.*?' : '.*?',"
replacement = r"subtitle: Text(_sleepTimerMinutes > 0 ? 'Còn lại $_sleepTimerMinutes phút' : 'Đang tắt',"

content = re.sub(pattern, replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen subtitle")
