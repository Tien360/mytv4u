import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("_startInlineTrailer() async {")
if idx != -1:
    print(content[idx:idx+2500])
