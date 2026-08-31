import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("void _generateRecommendations()")
if idx != -1:
    print(content[idx:idx+800])
