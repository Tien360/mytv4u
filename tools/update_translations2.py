
import json
files = ['assets/langs/en.json', 'assets/langs/vi.json']
new_keys = {
    'en.json': {
        'stream_disconnected': 'Stream disconnected. Please try again!',
    },
    'vi.json': {
        'stream_disconnected': 'Luồng bị ngắt kết nối. Vui lòng thử lại!',
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
print('Updated translations')

