import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor

with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_channels = []
current_channel = {}
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)
        logo = logo_match.group(1) if logo_match else ''
        display_name = line.split(',')[-1].strip()
        current_channel = {'name': display_name, 'logo': logo}
    elif line and not line.startswith('#'):
        current_channel['url'] = line
        m3u_channels.append(current_channel)
        current_channel = {}

target_kws = ['VTV', 'HTV', 'THVL', 'SCTV', 'VTC', 'K+']
to_check = [c for c in m3u_channels if any(kw in c['name'].upper() for kw in target_kws)]

def check_stream(ch):
    try:
        r = requests.head(ch['url'], timeout=5, allow_redirects=True)
        if r.status_code < 400:
            return ch, True
        r = requests.get(ch['url'], timeout=5, stream=True)
        return ch, r.status_code < 400
    except:
        return ch, False

alive_channels = []
with ThreadPoolExecutor(max_workers=20) as executor:
    for ch, is_alive in executor.map(check_stream, to_check):
        if is_alive:
            alive_channels.append(ch)

with open('alive_channels.json', 'w', encoding='utf-8') as f:
    json.dump(alive_channels, f, ensure_ascii=False, indent=2)

print("Done checking streams.")
