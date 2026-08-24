import urllib.request

url = "https://tinhlagi.pro/sport/lich-thi-dau.php"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    with open('lich_html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved lich_html.txt. Length:", len(html))
except Exception as e:
    print("Error:", e)
