with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()
idx = content.find("if (_directorsTmdb.isNotEmpty)")
if idx != -1:
    print(content[idx:idx+2500].encode('ascii', 'ignore').decode('ascii'))
