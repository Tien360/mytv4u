import requests
from bs4 import BeautifulSoup
r = requests.get('https://tinhlagi.pro/tivi/')
soup = BeautifulSoup(r.text, 'html.parser')
channels = []
for a in soup.find_all('a', class_='channel-card'):
    name = a.find(class_='channel-name').text.strip() if a.find(class_='channel-name') else 'Unknown'
    channels.append(name)

for c in channels:
    if 'SCTV' in c.upper() or 'HTV' in c.upper():
        print(c)
print(f"Total scraped channels: {len(channels)}")
