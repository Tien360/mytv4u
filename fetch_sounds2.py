import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "minion_hello.mp3": "https://www.myinstants.com/media/sounds/minions-bello.mp3",
    "minion_kiss.mp3": "https://www.myinstants.com/media/sounds/minion-kiss.mp3",
    "minion_yay.mp3": "https://www.myinstants.com/media/sounds/minion-yay.mp3"
}

out_dir = r"T:\Project\Phim\mytv4u_flutter\assets\easter\sfx"

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(os.path.join(out_dir, name), 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
