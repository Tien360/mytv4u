import json
import re
files = ['assets/langs/en.json', 'assets/langs/vi.json']
new_keys = {
    'en.json': {
        'app_disabled': 'Application has been disabled',
        'contact_developer': 'Please contact the developer.'
    },
    'vi.json': {
        'app_disabled': 'Ứng dụng đã ngừng hoạt động',
        'contact_developer': 'Vui lòng liên hệ nhà phát triển.'
    }
}
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    filename = file.split('/')[-1]
    for k, v in new_keys[filename].items():
        if k not in data:
            data[k] = v
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

with open('lib/screens/splash_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'Ứng dụng đã ngừng hoạt động'", "L10n.t('app_disabled')")
content = content.replace("'Vui lòng liên hệ nhà phát triển.'", "L10n.t('contact_developer')")
content = content.replace("'Thoát ứng dụng'", "L10n.t('exit_app')")

with open('lib/screens/splash_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done splash screen')
