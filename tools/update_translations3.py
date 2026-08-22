import json
files = ['assets/langs/en.json', 'assets/langs/vi.json']
new_keys = {
    'en.json': {
        'key_space': 'Space',
        'key_left_right': 'Left / Right Arrow',
        'key_up_down': 'Up / Down Arrow'
    },
    'vi.json': {
        'key_space': 'Space (Cách)',
        'key_left_right': 'Mũi tên Trái / Phải',
        'key_up_down': 'Mũi tên Lên / Xuống'
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

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'Space (Cách)'", "L10n.t('key_space') ?? 'Space (Cách)'")
content = content.replace("'Mũi tên Trái / Phải'", "L10n.t('key_left_right') ?? 'Mũi tên Trái / Phải'")
content = content.replace("'Mũi tên Lên / Xuống'", "L10n.t('key_up_down') ?? 'Mũi tên Lên / Xuống'")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
