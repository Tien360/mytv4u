import requests
import json
from concurrent.futures import ThreadPoolExecutor

with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_channels = []
current_channel = {}
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        display_name = line.split(',')[-1].strip()
        current_channel = {'display_name': display_name}
    elif line and not line.startswith('#'):
        current_channel['url'] = line
        m3u_channels.append(current_channel)
        current_channel = {}

# We only care about checking the streams of VTV, HTV, THVL, SCTV, VTC, and K+
target_kws = ['VTV', 'HTV', 'THVL', 'SCTV', 'VTC', 'K+']
to_check = [c for c in m3u_channels if any(kw in c['display_name'].upper() for kw in target_kws)]
print(f"Checking {len(to_check)} streams...")

def check_stream(ch):
    try:
        r = requests.head(ch['url'], timeout=5, allow_redirects=True)
        if r.status_code < 400:
            return ch['display_name'], True
        r = requests.get(ch['url'], timeout=5, stream=True)
        return ch['display_name'], r.status_code < 400
    except:
        return ch['display_name'], False

results = []
with ThreadPoolExecutor(max_workers=20) as executor:
    for name, is_alive in executor.map(check_stream, to_check):
        if is_alive:
            results.append(name)

print(f"Alive: {len(results)}")
print(results[:30])
