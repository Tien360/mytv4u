
from bs4 import BeautifulSoup
with open('onflix.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

slides = soup.find_all(class_=lambda c: c and 'slide' in c.lower())
if slides:
    for slide in slides[:2]:
        print('--- SLIDE ---')
        print(slide.prettify()[:500])

