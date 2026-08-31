import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/models/movie.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("server_data")
if idx != -1:
    print(content[idx-100:idx+600])
