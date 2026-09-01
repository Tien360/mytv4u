import urllib.request
import urllib.parse
import json

text = "In the aftermath of the devastating attack on King's Landing, Daenerys must face the survivors."
url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=" + urllib.parse.quote(text)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        translated = "".join([x[0] for x in data[0]])
        print("Success, length:", len(translated))
except Exception as e:
    print("Error:", e)
