import requests
from bs4 import BeautifulSoup
import re
import codecs

with codecs.open('our_channels_full.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

our_ids = []
our_names = []
for line in lines:
    match = re.search(r'\[(.*?)\] (.+)', line)
    if match:
        our_ids.append(match.group(1).strip().lower())
        our_names.append(match.group(2).strip().lower().replace('hd', '').strip())

r = requests.get('https://tinhlagi.pro/tivi/')
soup = BeautifulSoup(r.text, 'html.parser')
tinhlagi_added = []
for a in soup.find_all('a', class_='channel-card'):
    name_el = a.find(class_='channel-name')
    if name_el:
        orig = name_el.text.strip()
        t_clean = re.sub(r'[^a-z0-9]', '', orig.lower().replace('hd', ''))
        
        is_in = False
        for i in range(len(our_ids)):
            o_id = our_ids[i]
            o_name = re.sub(r'[^a-z0-9]', '', our_names[i])
            if o_name == t_clean or o_id == t_clean or o_id in t_clean:
                is_in = True
                break
        
        if not is_in:
            tinhlagi_added.append(orig)

print(f"Tinhlagi truly added: {len(tinhlagi_added)}")
with codecs.open('tinhlagi_added_strict.txt', 'w', encoding='utf-8') as f:
    for name in tinhlagi_added:
        f.write(name + "\n")
