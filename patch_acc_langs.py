import json

def patch(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'vi.json' in file:
        data['sync_status'] = 'TRẠNG THÁI KẾT NỐI:'
        data['sync_firebase'] = 'Dữ liệu cá nhân trên Firebase'
        data['sync_yt'] = 'YouTube (Gợi ý Cá nhân hóa)'
        data['btn_disconnect'] = 'Ngắt kết nối'
        data['btn_connect'] = 'Kết nối'
    else:
        data['sync_status'] = 'CONNECTION STATUS:'
        data['sync_firebase'] = 'Personal data on Firebase'
        data['sync_yt'] = 'YouTube (Personalized Recommendations)'
        data['btn_disconnect'] = 'Disconnect'
        data['btn_connect'] = 'Connect'

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch('assets/langs/vi.json')
patch('assets/langs/en.json')
