import json

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

import re
matches = re.finditer(r'.{0,50}(tuổi|age|rating|giới hạn).{0,50}', data, re.IGNORECASE)
for i, m in enumerate(matches):
    print(m.group(0))
    if i > 5:
        break
