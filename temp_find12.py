with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("L10n.t('watch_limit')")
if idx != -1:
    print(repr(content[idx-100:idx+50]))
