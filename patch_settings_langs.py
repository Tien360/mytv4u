import json

def patch(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'vi.json' in file:
        data['setting_opt_desc'] = 'Phân tích phần cứng và đề xuất thiết lập hiệu năng'
        data['setting_opt_btn'] = 'Quét ngay'
        
        data['setting_min_title'] = 'Giao diện tối giản (Máy yếu)'
        data['setting_min_desc'] = 'Tắt các hiệu ứng gương kính (kính mờ), giúp app chạy cực nhẹ trên máy tính cũ'
        
        data['setting_amb_title'] = 'Hình nền mờ Ambient'
        data['setting_amb_desc'] = 'Hiển thị hình nền mờ từ poster phim giúp giao diện sống động hơn'
        
        data['setting_egg_title'] = 'Bật hiệu ứng Easter Egg'
        data['setting_egg_desc'] = 'Nhấn vào thanh trạng thái tập ở bất kỳ phim nào để quay thưởng hiệu ứng! 4 cấp độ từ Phổ biến đến Huyền thoại (tỉ lệ 1%). Chúc may mắn!'
    else:
        data['setting_opt_desc'] = 'Analyze hardware and suggest best performance settings'
        data['setting_opt_btn'] = 'Scan now'
        
        data['setting_min_title'] = 'Minimalist UI (Low-end PC)'
        data['setting_min_desc'] = 'Disable all glassmorphism effects, making the app run incredibly smooth on older PCs'
        
        data['setting_amb_title'] = 'Ambient Background'
        data['setting_amb_desc'] = 'Show a blurred background from the movie poster to make the UI more lively'
        
        data['setting_egg_title'] = 'Enable Easter Egg Effects'
        data['setting_egg_desc'] = 'Tap the episode status line on any movie to spin for effects! 4 tiers from Common to Legendary (1% chance). Good luck!'

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch('assets/langs/vi.json')
patch('assets/langs/en.json')
