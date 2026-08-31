import json
import codecs

def update_json(filepath, key, value):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        data = json.load(f)
    data[key] = value
    with codecs.open(filepath, 'w', 'utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json('assets/langs/vi.json', 'opt_apply_audio', 'Tắt hiệu ứng Trình phát Nhạc (Tiết kiệm pin)')
update_json('assets/langs/vi.json', 'opt_apply_audio_sub', 'Tắt Sóng âm và Đĩa than xoay giúp giảm tải CPU/GPU, kéo dài thời lượng sử dụng pin.')

update_json('assets/langs/en.json', 'opt_apply_audio', 'Disable Audio Player Effects (Battery Saver)')
update_json('assets/langs/en.json', 'opt_apply_audio_sub', 'Disables Visualizer and spinning Vinyl to reduce CPU/GPU load and extend battery life.')

