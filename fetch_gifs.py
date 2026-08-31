import urllib.request
import json
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_tenor(query):
    # Public tenor API key for testing
    url = f"https://g.tenor.com/v1/search?q={urllib.parse.quote(query)}&key=LIVDSRZULELA&limit=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read())
        if data['results']:
            return data['results'][0]['media'][0]['gif']['url']
    except Exception as e:
        print(f"Error: {e}")
    return None

print("Spray:", search_tenor("minion spray paint"))
print("Guitar:", search_tenor("minion guitar"))
print("Confused:", search_tenor("minion confused question mark"))
