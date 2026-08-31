import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("Future<void> _applyOptimization()")
if idx != -1:
    print(content[idx+800:idx+2500])
