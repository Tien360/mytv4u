import json
import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    dart_code = f.read()

with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    vi_json = json.load(f)

used_keys = set(re.findall(r"'([a-z0-9_]+)'", dart_code))
missing = []
for key in used_keys:
    if key.startswith("ep_msg") or key.startswith("easter_"):
        if key not in vi_json:
            missing.append(key)

print("Missing:", missing)
