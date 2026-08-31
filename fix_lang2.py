import json
def update_json(file, key, val):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[key] = val
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json('assets/langs/vi.json', 'audio_player_title', 'Trình phát Nhạc')
update_json('assets/langs/en.json', 'audio_player_title', 'Audio Player')
