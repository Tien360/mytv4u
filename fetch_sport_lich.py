import urllib.request
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = "https://tinhlagi.pro/sport/lich-thi-dau.php"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        print("Iframe src:", iframe.get('src'))
        
except Exception as e:
    print("Error:", e)
