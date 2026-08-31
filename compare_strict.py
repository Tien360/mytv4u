import requests
from bs4 import BeautifulSoup
import json
import re

# 1. Parse M3U
with open('vmttv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

m3u_names = []
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        m3u_names.append(line.split(',')[-1].strip())

# 2. Scrape tinhlagi
r = requests.get('https://tinhlagi.pro/tivi/')
soup = BeautifulSoup(r.text, 'html.parser')
tinhlagi_names = []
for a in soup.find_all('a', class_='channel-card'):
    name_el = a.find(class_='channel-name')
    if name_el:
        tinhlagi_names.append(name_el.text.strip())

# 3. Simple lowercasing and stripping
m3u_simple = set([n.lower().strip() for n in m3u_names])
tinhlagi_simple = set([n.lower().strip() for n in tinhlagi_names])

tinhlagi_only = [n for n in tinhlagi_names if n.lower().strip() not in m3u_simple]

print(f"Strict match Tinhlagi ONLY: {len(tinhlagi_only)}")
for n in tinhlagi_only[:20]:
    print(n.encode('utf-8').decode('utf-8', 'ignore'))
