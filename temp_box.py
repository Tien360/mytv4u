content = open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8').read()
idx = content.find("CheckboxListTile(")
open('temp.txt', 'w', encoding='utf-8').write(content[idx:idx+1500])
