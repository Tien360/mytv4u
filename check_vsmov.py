import urllib.request
import json
try:
    req = urllib.request.Request('https://vsmov.com/api/danh-sach/phim-moi-cap-nhat?page=1')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    first_slug = data['items'][0]['slug']
    print(first_slug)
    
    req2 = urllib.request.Request(f'https://vsmov.com/api/phim/{first_slug}')
    response2 = urllib.request.urlopen(req2)
    data2 = json.loads(response2.read().decode('utf-8'))
    ep = data2['episodes'][0]['server_data'][0]
    print(f"m3u8: {ep.get('link_m3u8', '')}")
    print(f"embed: {ep.get('link_embed', '')}")
except Exception as e:
    print(e)
