import requests
from bs4 import BeautifulSoup
import re
import json

# 1. Parse M3U (User's channels)
with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_names = []
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        display_name = line.split(',')[-1].strip()
        m3u_names.append(display_name)

# 2. Scrape tinhlagi
r = requests.get('https://tinhlagi.pro/tivi/')
soup = BeautifulSoup(r.text, 'html.parser')
tinhlagi_names = []
for a in soup.find_all('a', class_='channel-card'):
    name_el = a.find(class_='channel-name')
    if name_el:
        tinhlagi_names.append(name_el.text.strip())

# 3. Clean and compare
def clean(name):
    return re.sub(r'[^a-z0-9]', '', name.lower().replace('hd', '').replace('vinhlong', 'vl'))

m3u_clean = {clean(n): n for n in m3u_names}
tinhlagi_clean = {clean(n): n for n in tinhlagi_names}

tinhlagi_only = []
for clean_name, orig_name in tinhlagi_clean.items():
    if clean_name not in m3u_clean:
        tinhlagi_only.append(orig_name)

m3u_only = []
for clean_name, orig_name in m3u_clean.items():
    if clean_name not in tinhlagi_clean:
        m3u_only.append(orig_name)

with open('tinhlagi_only.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(tinhlagi_only))

with open('m3u_only.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(m3u_only))

print(f"Total M3U: {len(m3u_names)}")
print(f"Total Tinhlagi: {len(tinhlagi_names)}")
print(f"Tinhlagi ONLY: {len(tinhlagi_only)}")
print(f"M3U ONLY: {len(m3u_only)}")
