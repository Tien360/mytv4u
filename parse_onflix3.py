
from bs4 import BeautifulSoup
with open('onflix.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

slides = soup.find_all('div', class_=lambda c: c and 'swiper-slide' in c.lower())
with open('onflix_out.txt', 'w', encoding='utf-8') as f:
    for slide in slides[:2]:
        f.write('--- SLIDE ---\n')
        f.write(slide.prettify())

