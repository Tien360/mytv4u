import re
import requests

# 1. Parse M3U file
with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_channels = []
current_channel = {}
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        # Extract tvg-name
        name_match = re.search(r'tvg-name="([^"]+)"', line)
        # Extract tvg-logo
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)
        # Extract group-title
        group_match = re.search(r'group-title="([^"]+)"', line)
        # Extract display name (after the comma)
        display_name = line.split(',')[-1].strip()
        
        current_channel = {
            'tvg_name': name_match.group(1) if name_match else display_name,
            'tvg_logo': logo_match.group(1) if logo_match else '',
            'group_title': group_match.group(1) if group_match else '',
            'display_name': display_name
        }
    elif line and not line.startswith('#'):
        current_channel['url'] = line
        m3u_channels.append(current_channel)
        current_channel = {}

print(f"Parsed {len(m3u_channels)} channels from M3U.")

# 2. Parse our existing channels
with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    dart_code = f.read()

our_channels = []
channel_blocks = re.findall(r'TvChannel\((.*?)\)', dart_code, re.DOTALL)
for block in channel_blocks:
    id_match = re.search(r"id:\s*'([^']+)'", block)
    name_match = re.search(r"name:\s*'([^']+)'", block)
    logo_match = re.search(r"logo:\s*'([^']+)'", block)
    
    if id_match and name_match:
        our_channels.append({
            'id': id_match.group(1),
            'name': name_match.group(1),
            'logo': logo_match.group(1) if logo_match else ''
        })

print(f"Parsed {len(our_channels)} channels from tv_api.dart.")

# 3. Find matches and logo updates
updates = []
for our in our_channels:
    # Try to find a match in M3U by name
    # Clean names for better matching
    our_clean = our['name'].lower().replace('hd', '').strip()
    for m3u in m3u_channels:
        m3u_clean = m3u['display_name'].lower().replace('hd', '').strip()
        if our_clean == m3u_clean or our['id'].lower() == m3u['tvg_name'].lower() or our['id'].lower() in m3u_clean.replace(' ', ''):
            if m3u['tvg_logo'] and m3u['tvg_logo'] != our['logo']:
                updates.append((our['name'], our['logo'], m3u['tvg_logo']))
            break

print(f"Found {len(updates)} logos to update.")

# 4. Find missing channels in our list
missing = []
our_names_clean = [c['name'].lower().replace('hd', '').replace(' ', '') for c in our_channels]
our_ids = [c['id'].lower() for c in our_channels]

for m3u in m3u_channels:
    m3u_name_clean = m3u['display_name'].lower().replace('hd', '').replace(' ', '')
    # Check if this channel is in our list
    is_in_our_list = False
    for our in our_channels:
        our_c = our['name'].lower().replace('hd', '').replace(' ', '')
        if m3u_name_clean == our_c or m3u['tvg_name'].lower() == our['id'].lower() or our['id'].lower() in m3u_name_clean:
            is_in_our_list = True
            break
            
    if not is_in_our_list:
        # Avoid local/spam channels, only keep VTV, HTV, THVL, SCTV, VTVCab, or popular ones
        title = m3u['display_name'].upper()
        if any(x in title for x in ['VTV', 'HTV', 'THVL', 'SCTV', 'VTC', 'BONG DA', 'THE THAO', 'K+', 'HBO', 'CINEMAX']):
            missing.append(m3u)

print(f"Found {len(missing)} potentially interesting missing channels.")
for m in missing[:20]:
    print(m['display_name'].encode('utf-8').decode('utf-8', 'ignore'))
