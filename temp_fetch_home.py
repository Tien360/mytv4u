import urllib.request

req = urllib.request.Request(
    'https://www.youtube.com/playables',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
    }
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    with open('yt_playables_home.html', 'w', encoding='utf-8') as f:
        f.write(html)
print("Saved home page")
