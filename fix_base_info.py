with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("_buildRichText(\n                                              L10n.t('genres'),", "_buildRichText(\n                                              '${L10n.t('genres')}: ',")
content = content.replace("_buildRichText(\n                                              L10n.t('directors'),", "_buildRichText(\n                                              '${L10n.t('directors')}: ',")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Base info fixed")
