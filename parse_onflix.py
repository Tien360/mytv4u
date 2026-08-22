
from bs4 import BeautifulSoup
with open('onflix.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
# Find hero banner or swiper
# Look for images inside swiper-slide or main banner
banners = soup.find_all('div', class_=lambda c: c and 'banner' in c.lower())
if not banners:
    banners = soup.find_all('div', class_=lambda c: c and 'hero' in c.lower())

for img in soup.find_all('img'):
    src = img.get('src', '')
    if 'logo' in src.lower() or 'title' in src.lower() or 'clear' in src.lower():
        print(src)

