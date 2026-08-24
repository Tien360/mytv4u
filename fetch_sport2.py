import urllib.request
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = "https://tinhlagi.pro/sport/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    print("Page Title:", soup.title.string if soup.title else "No title")
    
    print("\n--- Examining tabs/sections ---")
    navs = soup.find_all('ul', class_='nav')
    for nav in navs:
        print("Nav:", nav.get_text(strip=True, separator=' | '))
        
    print("\n--- Examining iframe or specific content ---")
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        print("Iframe src:", iframe.get('src'))
        
    print("\n--- Checking for 'Lịch Thi Đấu' or 'Tỷ Số' ---")
    for elem in soup.find_all(string=lambda text: text and ('Lịch' in text or 'Tỷ số' in text or 'Lịch Thi Đấu' in text or 'Kết quả' in text)):
        print("Found text:", elem.strip())
        parent = elem.parent
        print("Parent tag:", parent.name, parent.attrs)
        
except Exception as e:
    print("Error:", e)
