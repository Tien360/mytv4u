import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("L10n.t('default_speed')")
if idx != -1:
    print(content[idx-5000:idx-4000])
