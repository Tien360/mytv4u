import json

def patch(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'vi.json' in file:
        data['nav_library'] = 'Thư viện'
        data['favorite_list'] = 'Thư viện cá nhân'
        data['favorite_empty'] = 'Bạn chưa lưu phim nào trong thư viện.'
        data['lib_open_link'] = 'Mở Link (Web)'
        data['lib_open_file'] = 'Mở File (Máy tính)'
        data['lib_link_dialog_title'] = 'Mở đường dẫn mạng (URL)'
        data['lib_link_dialog_hint'] = 'Nhập link mp4, m3u8, hoặc YouTube...'
        data['lib_link_dialog_live'] = 'Đánh dấu là luồng trực tiếp (Live)'
        data['lib_link_dialog_cancel'] = 'Hủy'
        data['lib_link_dialog_open'] = 'Phát ngay'
    else:
        data['nav_library'] = 'Library'
        data['favorite_list'] = 'Personal Library'
        data['favorite_empty'] = 'Your library is currently empty.'
        data['lib_open_link'] = 'Open Link (Web)'
        data['lib_open_file'] = 'Open File (Local)'
        data['lib_link_dialog_title'] = 'Open Network Stream (URL)'
        data['lib_link_dialog_hint'] = 'Enter mp4, m3u8, or YouTube link...'
        data['lib_link_dialog_live'] = 'Mark as Live Stream'
        data['lib_link_dialog_cancel'] = 'Cancel'
        data['lib_link_dialog_open'] = 'Play'

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch('assets/langs/vi.json')
patch('assets/langs/en.json')
