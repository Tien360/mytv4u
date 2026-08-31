import json

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

import re
matches = re.findall(r'everyone|teen|mature|\+10|10\+|12\+|16\+|18\+|PEGI|ESRB', data, re.IGNORECASE)
print(set(matches))
