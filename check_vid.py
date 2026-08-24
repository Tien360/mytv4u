import urllib.request
import re
html = urllib.request.urlopen("https://www.youtube.com/watch?v=3wLbYR1ZzFU").read().decode('utf-8')
match = re.search(r'<title>(.*?)</title>', html)
if match: print("Title:", match.group(1))
