import json
import re

with open('alive_channels.json', 'r', encoding='utf-8') as f:
    alive = json.load(f)

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    dart_code = f.read()

channel_blocks = re.findall(r'(TvChannel\([^)]+\))', dart_code, re.DOTALL)
our_channels = []
for block in channel_blocks:
    id_match = re.search(r"id:\s*'([^']+)'", block)
    name_match = re.search(r"name:\s*'([^']+)'", block)
    if id_match and name_match: 
        our_channels.append({
            'id': id_match.group(1).lower(),
            'name': name_match.group(1).lower().replace('hd', '').strip()
        })

missing = []
for ch in alive:
    m3u_name = ch['name'].lower().replace('hd', '').strip()
    is_in = False
    for our in our_channels:
        if m3u_name == our['name'] or our['id'] == m3u_name.replace(' ', '') or our['id'] in m3u_name.replace(' ', ''):
            is_in = True
            break
    if not is_in:
        missing.append(ch)

with open('missing.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)

print(f"Missing alive channels: {len(missing)}")
