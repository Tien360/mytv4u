import json

files = ['assets/langs/vi.json', 'assets/langs/en.json']
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if file == 'assets/langs/vi.json':
        data['audio_player_title'] = "Trình phát Nhạc"
        data['audio_visualizer'] = "Hiệu ứng Sóng âm"
        data['viz_none'] = "Tắt"
        data['viz_inline'] = "Nhỏ (Cạnh tên)"
        data['viz_bars'] = "Lớn (Dưới ảnh)"
        data['audio_vinyl'] = "Hiệu ứng Đĩa than"
        data['audio_vinyl_desc'] = "Mô phỏng đĩa than xoay khi phát nhạc"
        data['audio_sleep_timer'] = "Hẹn giờ tắt (Phút)"
        data['timer_off'] = "Tắt"
        data['player_settings'] = "Trình phát Phim"
        data['video_player'] = "Trình phát Phim"
    else:
        data['audio_player_title'] = "Audio Player"
        data['audio_visualizer'] = "Audio Visualizer"
        data['viz_none'] = "Off"
        data['viz_inline'] = "Inline (Next to name)"
        data['viz_bars'] = "Large (Below cover)"
        data['audio_vinyl'] = "Vinyl Effect"
        data['audio_vinyl_desc'] = "Simulate spinning vinyl record"
        data['audio_sleep_timer'] = "Sleep Timer (Minutes)"
        data['timer_off'] = "Off"
        data['player_settings'] = "Video Player"
        data['video_player'] = "Video Player"
        
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated translation files with audio keys!")
