import urllib.request
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = "https://tinhlagi.pro/sport/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    matches = soup.find_all(class_='match-btn')
    print(f"Found {len(matches)} matches.")
    # Find ones without 'status-live'
    for btn in matches:
        title = btn.get('data-title', '')
        time = btn.get('data-time', '')
        
        status_badge = btn.find(class_='status-badge')
        status_text = status_badge.get_text(strip=True) if status_badge else "No badge"
        status_classes = status_badge.get('class') if status_badge else []
        
        if 'status-live' not in status_classes:
            print(f"NOT LIVE Match: {title} | Time: {time}")
            print(f"  Badge Text: {status_text} | Badge Classes: {status_classes}")
            
except Exception as e:
    print("Error:", e)
