with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("L10n.t('actors')")
if idx != -1:
    print(content[idx+2000:idx+4500])
