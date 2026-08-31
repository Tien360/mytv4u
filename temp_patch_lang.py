import json

files = ['assets/langs/vi.json', 'assets/langs/en.json']
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if file == 'assets/langs/vi.json':
        data['setting_opt_title'] = "Trợ lý Tối ưu hóa (Khuyên dùng)"
        data['skip_intro_duration'] = "Thời lượng bỏ qua"
        data['background_playback'] = "Phát dưới nền"
        data['background_playback_sub'] = "Tiếp tục phát âm thanh khi ẩn ứng dụng"
    else:
        data['setting_opt_title'] = "Optimizer Assistant (Recommended)"
        data['skip_intro_duration'] = "Skip duration"
        data['background_playback'] = "Background playback"
        data['background_playback_sub'] = "Continue playing audio when app is hidden"
        
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated translation files!")
