import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("_pauseTrailer(")
if idx != -1:
    print(content[idx-50:idx+400])
