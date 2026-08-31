import json

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

import re
matches = re.findall(r'tuổi|age|rating|giới hạn', data, re.IGNORECASE)
print(set(matches))
