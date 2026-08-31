import json

files = ['assets/langs/vi.json', 'assets/langs/en.json']
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if file == 'assets/langs/vi.json':
        data['visualizer_type'] = "Kiểu sóng âm"
        data['vinyl_effect'] = "Hiệu ứng Đĩa than"
        data['sleep_timer'] = "Hẹn giờ tắt (Phút)"
        data['off'] = "Tắt"
        data['viz_circle'] = "Vòng tròn đĩa"
    else:
        data['visualizer_type'] = "Visualizer Type"
        data['vinyl_effect'] = "Vinyl Effect"
        data['sleep_timer'] = "Sleep Timer (Minutes)"
        data['off'] = "Off"
        data['viz_circle'] = "Disc Circle"
        
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated translation files with audio keys!")
