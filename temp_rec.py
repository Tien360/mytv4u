content = open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8').read()
idx = content.find("_buildRecommendations()")
print(content[idx:idx+1500])
