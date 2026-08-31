import json
with open("T:/Project/Phim/mytv4u_flutter/assets/langs/vi.json", "r", encoding="utf-8") as f:
    data = json.load(f)
for k, v in data.items():
    if k in ['cancel', 'open', 'library', 'close']:
        print(f"{k}: {v}")
