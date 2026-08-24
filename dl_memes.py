import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

try:
    urllib.request.urlretrieve("https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png", "assets/easter/trollface.png")
    print("Downloaded Trollface.")
except Exception as e:
    print(e)
