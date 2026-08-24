import urllib.request
import json
import sys
import ssl

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

slug = "su-huynh-qua-can-trong"
urls = [
    ("NguonC", f"https://phim.nguonc.com/api/film/{slug}"),
    ("KKPhim", f"https://phimapi.com/phim/{slug}"),
    ("OPhim", f"https://ophim1.com/phim/{slug}"),
    ("VSMov", f"https://vsmcamp.com/api/movie/{slug}"),
    ("Phim4K", f"https://phim4k.net/api/movie/{slug}"),
    ("Free1", f"https://dev2024.oxaliplatin.workers.dev/api/movies/{slug}"),
    ("Premium", f"https://dogtail.oxaliplatin.workers.dev/api/premium/detail/{slug}")
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        data = json.loads(res)
        movie = data.get('movie', data.get('item', data.get('data', {}).get('item', {})))
        print(f"{name}:", repr(movie.get('name')))
    except Exception as e:
        print(f"{name}: ERROR {e}")
