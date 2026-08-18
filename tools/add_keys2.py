import json

def update_json(filepath, additions):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for k, v in additions.items():
        data[k] = v
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json('assets/langs/vi.json', {
    'global_color_settings': 'Màu sắc toàn cục',
    'sources': 'Nguồn phim',
    'system_settings': 'Trình phát & Hệ thống',
    'health_utilities': 'Sức khỏe & Tiện ích'
})

update_json('assets/langs/en.json', {
    'global_color_settings': 'Global Color Settings',
    'sources': 'Movie Sources',
    'system_settings': 'Player & System',
    'health_utilities': 'Health & Utilities'
})

print("Done")
