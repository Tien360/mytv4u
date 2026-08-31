import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "minion_laugh.mp3": "https://www.myinstants.com/media/sounds/minions-laughing.mp3",
    "minion_banana.mp3": "https://www.myinstants.com/media/sounds/banana-song-minions.mp3",
    "minion_what.mp3": "https://www.myinstants.com/media/sounds/minion-what.mp3"
}

import os
out_dir = r"T:\Project\Phim\mytv4u_flutter\assets\easter\sfx"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(os.path.join(out_dir, name), 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
