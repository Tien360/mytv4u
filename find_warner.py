import urllib.request
try:
    req = urllib.request.Request('https://raw.githubusercontent.com/PhungKhai/IPTV-VN/master/live.m3u', headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    lines = response.read().decode('utf-8').splitlines()
    for i, line in enumerate(lines):
        if 'warner' in line.lower():
            print(line)
            print(lines[i+1])
except Exception as e:
    print(e)
