import json

paths = ['assets/langs/vi.json', 'assets/langs/en.json']

new_keys_vi = {
  "viz_none": "Tắt",
  "viz_inline": "Nhỏ (cạnh tên)",
  "viz_bars": "Lớn (dưới ảnh)",
  "viz_circle": "Vòng tròn đĩa",
  "audio_settings": "Cài đặt Trình phát",
  "visualizer_type": "Kiểu sóng âm",
  "sleep_timer": "Hẹn giờ tắt (phút)",
  "off": "Tắt",
  "repeat_mode": "Chế độ lặp lại",
  "repeat_none": "Không lặp",
  "repeat_all": "Lặp danh sách",
  "repeat_one": "Lặp 1 bài",
  "shortcuts": "Phím tắt",
  "audio_quality": "Chất lượng âm thanh",
  "unknown": "Chưa rõ",
  "error_read_file": "Lỗi đọc file",
  "vinyl_effect": "Hiệu ứng Đĩa than",
  "playlist": "Danh sách phát",
  "unknown_track": "Unknown Track",
  "unknown_artist": "Unknown Artist",
  "shuffle": "Trộn bài",
  "prev": "Bài trước",
  "play_pause": "Phát/Tạm dừng",
  "next": "Bài tiếp",
  "repeat": "Lặp lại",
  "settings": "Cài đặt",
  "add_to_playlist": "Thêm nhạc"
}

new_keys_en = {
  "viz_none": "None",
  "viz_inline": "Small (Inline)",
  "viz_bars": "Large (Bottom)",
  "viz_circle": "Circular",
  "audio_settings": "Player Settings",
  "visualizer_type": "Visualizer Type",
  "sleep_timer": "Sleep Timer (mins)",
  "off": "Off",
  "repeat_mode": "Repeat Mode",
  "repeat_none": "No Repeat",
  "repeat_all": "Repeat All",
  "repeat_one": "Repeat One",
  "shortcuts": "Shortcuts",
  "audio_quality": "Audio Quality",
  "unknown": "Unknown",
  "error_read_file": "Error reading file",
  "vinyl_effect": "Vinyl Effect",
  "playlist": "Playlist",
  "unknown_track": "Unknown Track",
  "unknown_artist": "Unknown Artist",
  "shuffle": "Shuffle",
  "prev": "Previous",
  "play_pause": "Play/Pause",
  "next": "Next",
  "repeat": "Repeat",
  "settings": "Settings",
  "add_to_playlist": "Add to Playlist"
}

for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'vi' in path:
        for k, v in new_keys_vi.items():
            if k not in data:
                data[k] = v
    else:
        for k, v in new_keys_en.items():
            if k not in data:
                data[k] = v
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

