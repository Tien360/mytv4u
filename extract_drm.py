import re
import json
import urllib.parse

with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

channels = []
current_logo = ""
current_name = ""
current_id = ""
current_group = ""
current_drm_key = ""

for line in lines:
    line = line.strip()
    if line.startswith("#EXTINF:"):
        # reset
        current_drm_key = ""
        # parse tvg-logo
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)
        current_logo = logo_match.group(1) if logo_match else ""
        
        name_match = re.search(r',(.+)$', line)
        current_name = name_match.group(1).strip() if name_match else "Unknown"
        
        id_match = re.search(r'tvg-id="([^"]+)"', line)
        current_id = id_match.group(1) if id_match else current_name
        
        group_match = re.search(r'group-title="([^"]+)"', line)
        current_group = group_match.group(1) if group_match else "Khác"
        
    elif line.startswith("#KODIPROP:inputstream.adaptive.license_key="):
        current_drm_key = line.split("=", 1)[1]
    
    elif line.startswith("http") and ".mpd" in line:
        channels.append({
            "id": current_id,
            "name": current_name,
            "logo": current_logo,
            "group": current_group,
            "url": line,
            "drm_key": current_drm_key
        })

print(f"Found {len(channels)} MPD channels.")
for c in channels:
    if c['drm_key']:
        print(f"{c['name']} -> {c['drm_key'][:30]}...")

