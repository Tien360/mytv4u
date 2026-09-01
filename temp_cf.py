import urllib.request
import json
import ssl

def check_domain(domain):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(f"https://{domain}", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return str(e)

domains = ["film4k.vip", "film4k.live", "film4k.me", "film4k.cc", "phim4k.net"]
for d in domains:
    print(d, check_domain(d))
