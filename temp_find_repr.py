import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("_isWebviewInitialized = true")
if idx != -1:
    print(repr(content[idx-60:idx+60]))
