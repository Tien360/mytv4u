import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "rasengan.mp3": "https://www.myinstants.com/media/sounds/rasengan-sound.mp3",
    "kage_bunshin.mp3": "https://www.myinstants.com/media/sounds/kage-bunshin-no-jutsu_l6mXyM0.mp3",
    "sharingan.mp3": "https://www.myinstants.com/media/sounds/sharingan-sound-effect.mp3",
    "puff.mp3": "https://www.myinstants.com/media/sounds/naruto-teleport.mp3", # Or similar jutsu sound
    "ramen_slurp.mp3": "https://www.myinstants.com/media/sounds/slurp-loud.mp3",
    "jutsu.mp3": "https://www.myinstants.com/media/sounds/naruto-jutsu.mp3",
    "sexy_jutsu.mp3": "https://www.myinstants.com/media/sounds/naruto-sexy-jutsu.mp3"
}

out_dir = r"T:\Project\Phim\mytv4u_flutter\assets\easter\sfx"

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            with open(os.path.join(out_dir, name), 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
