import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
html = urllib.request.urlopen("https://www.youtube.com/watch?v=XtpMWvBnNmQ").read().decode('utf-8')
match = re.search(r'<title>(.*?)</title>', html)
if match: print("Title:", match.group(1))
