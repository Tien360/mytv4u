
import json

files = ['assets/langs/en.json', 'assets/langs/vi.json']

new_keys = {
    'en.json': {
        'keyboard_shortcuts': 'Keyboard Shortcuts',
        'shortcuts': 'Shortcuts',
        'shortcut_fullscreen': 'Fullscreen',
        'shortcut_escape': 'Exit Fullscreen',
        'shortcut_play_pause': 'Play / Pause',
        'shortcut_zoom': 'Fill mode',
        'shortcut_seek': 'Seek backward / forward 10s',
        'shortcut_volume': 'Volume Up / Down',
        'shortcut_mute': 'Mute / Unmute',
        'shortcut_next_episode': 'Next Episode',
        'video_quality': 'Video Quality'
    },
    'vi.json': {
        'keyboard_shortcuts': 'Phím tắt',
        'shortcuts': 'Phím tắt',
        'shortcut_fullscreen': 'Toàn màn hình',
        'shortcut_escape': 'Thoát toàn màn hình',
        'shortcut_play_pause': 'Phát / Tạm dừng',
        'shortcut_zoom': 'Chế độ lấp đầy',
        'shortcut_seek': 'Tua lùi / tới 10s',
        'shortcut_volume': 'Tăng / Giảm âm lượng',
        'shortcut_mute': 'Tắt / Mở tiếng',
        'shortcut_next_episode': 'Chuyển tập tiếp theo',
        'video_quality': 'Chất lượng video'
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

