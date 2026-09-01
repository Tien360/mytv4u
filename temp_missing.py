import json
import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    dart_code = f.read()

with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    vi_json = json.load(f)

used_keys = set(re.findall(r"'ep_msg_[a-z0-9_]+'", dart_code))
missing = []
for key in used_keys:
    clean_key = key.strip("'")
    if clean_key not in vi_json:
        missing.append(clean_key)

print("Missing in vi.json:", missing)
