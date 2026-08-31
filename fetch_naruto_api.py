import urllib.request
import urllib.parse
import ssl
import json
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_search(query, filename):
    url = f"https://www.myinstants.com/api/v1/instants/?name={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            data = json.loads(response.read())
            if data['results']:
                audio_url = data['results'][0]['sound']
                print(f"Found {query}: {audio_url}")
                
                req2 = urllib.request.Request(audio_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2, context=ctx, timeout=5) as r2:
                    with open(os.path.join(r"T:\Project\Phim\mytv4u_flutter\assets\easter\sfx", filename), 'wb') as f:
                        f.write(r2.read())
                print(f"Downloaded {filename}")
                return True
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return False

fetch_search("rasengan", "rasengan.mp3")
fetch_search("kage bunshin", "kage_bunshin.mp3")
fetch_search("sharingan", "sharingan.mp3")
fetch_search("naruto flute", "naruto_theme.mp3")
