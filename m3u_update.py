import re
import json

with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_channels = []
current_channel = {}
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)
        group_match = re.search(r'group-title="([^"]+)"', line)
        display_name = line.split(',')[-1].strip()
        current_channel = {
            'logo': logo_match.group(1) if logo_match else '',
            'group': group_match.group(1) if group_match else '',
            'name': display_name
        }
    elif line and not line.startswith('#'):
        current_channel['url'] = line
        m3u_channels.append(current_channel)
        current_channel = {}

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    dart_code = f.read()

our_channels = []
channel_blocks = re.findall(r'(TvChannel\([^)]+\))', dart_code, re.DOTALL)

updates = {}
for block in channel_blocks:
    id_match = re.search(r"id:\s*'([^']+)'", block)
    name_match = re.search(r"name:\s*'([^']+)'", block)
    if not id_match or not name_match: continue
    
    our_id = id_match.group(1)
    our_name = name_match.group(1).lower().replace('hd', '').strip()
    
    for m3u in m3u_channels:
        m3u_name = m3u['name'].lower().replace('hd', '').strip()
        # Find match
        if our_name == m3u_name or our_id == m3u_name.replace(' ', ''):
            if m3u['logo']:
                updates[our_id] = {'new_logo': m3u['logo'], 'new_url': m3u['url'], 'm3u_name': m3u['name']}
            break

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(updates, f, ensure_ascii=False, indent=2)

print("Saved updates to updates.json")
