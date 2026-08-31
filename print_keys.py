import json
with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    d = json.load(f)
for k in d.keys():
    if "ep_msg_" in k or "easter_" in k:
        print(k)
