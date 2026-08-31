import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "tom_scream.mp3": "https://www.myinstants.com/media/sounds/tom-scream.mp3",
    "bongo_run.mp3": "https://www.myinstants.com/media/sounds/bongo_run.mp3", # Or similar cartoon running sound
    "zap.mp3": "https://www.myinstants.com/media/sounds/electric_zap.mp3",
    "jerry_laugh.mp3": "https://www.myinstants.com/media/sounds/jerry-laugh.mp3",
    "cartoon_run.mp3": "https://www.myinstants.com/media/sounds/cartoon-running-sound-effect.mp3"
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
