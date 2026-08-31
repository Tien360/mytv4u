import json

def patch(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'vi.json' in file:
        data['opt_scan_sub'] = 'Kiểm tra Chip, RAM, Màn hình, Pin và Tốc độ mạng...'
        data['opt_specs'] = 'Khuyến cáo thông minh:'
        data['opt_spec_cpu'] = 'CPU'
        data['opt_spec_gpu'] = 'GPU'
        data['opt_spec_ram'] = 'RAM'
        data['opt_spec_screen'] = 'Màn hình'
        data['opt_spec_net'] = 'Tốc độ mạng'
        data['opt_net_err'] = 'Lỗi đo mạng'
        
        data['opt_high_end_title'] = 'Tuyệt vời!'
        data['opt_high_end_desc'] = 'Cấu hình của bạn đủ sức chơi video 4K, thoải mái bật các thiết lập đồ họa đẹp nhất của ứng dụng.'
        
        data['opt_low_end_title'] = 'Cấu hình khiêm tốn: '
        data['opt_low_end_desc'] = 'Hệ thống sẽ đề xuất tự động tắt bớt hiệu ứng kính mờ để trải nghiệm của bạn mượt mà nhất.'
        
        data['opt_std_title'] = 'Cấu hình tiêu chuẩn: '
        data['opt_std_desc'] = 'Máy tính của bạn hoàn toàn đáp ứng tốt để trải nghiệm video ở mức 1080p.'
        
        data['opt_bat_title'] = 'Đang dùng Pin: '
        data['opt_bat_desc'] = 'Nếu bạn muốn cày phim lâu hơn, hãy ưu tiên chọn chất lượng 1080p và đồng ý tắt bớt hiệu ứng nền (nếu có) để tiết kiệm điện.'
        
        data['opt_fhd_title'] = 'Màn hình Full HD: '
        data['opt_fhd_desc'] = 'Màn hình hiện tại không hiển thị được 4K, do đó bạn chỉ nên chọn video 1080p để tránh hao phí CPU vô ích.'
        
        data['opt_net_title'] = 'Mạng khá chậm'
        data['opt_net_desc'] = 'Bạn nên đổi mức chất lượng phát video mặc định về 720p hoặc 1080p để xem phim không bị gián đoạn.'
        
        data['opt_apply_title'] = 'Tự động áp dụng cài đặt giao diện (Tích chọn nếu muốn):'
        data['opt_apply_min'] = 'Bật Giao diện tối giản (Tắt 100% hiệu ứng kính mờ/gương)'
        data['opt_apply_min_sub'] = 'Giúp app chạy siêu mượt trên các máy tính đời cũ.'
        data['opt_apply_amb'] = 'Tắt hiệu ứng Hình nền mờ (Ambient Background)'
        data['opt_apply_amb_sub1'] = 'Giảm tải đáng kể cho GPU giúp tiết kiệm Pin và tăng thời gian sử dụng.'
        data['opt_apply_amb_sub2'] = 'Giải phóng tài nguyên đồ họa cho máy tính.'
        data['opt_apply_trl'] = 'Tắt Phát tự động Trailer'
        data['opt_apply_trl_sub1'] = 'Giảm số vòng xoay ổ cứng và mạng để tiết kiệm Pin.'
        data['opt_apply_trl_sub2'] = 'Giảm hiện tượng giật lag khi mở trang phim.'
        data['opt_apply_all'] = 'Bật TOÀN BỘ hiệu ứng rực rỡ nhất'
        data['opt_apply_all_sub'] = 'Máy tính của bạn hoàn toàn đủ khỏe để xử lý mọi đồ họa nặng nhất của app.'
        data['opt_apply_note'] = 'Máy ở mức tiêu chuẩn, bạn có thể tự tinh chỉnh các hiệu ứng trong Cài đặt tùy theo sở thích.'
        
        data['opt_btn_default'] = 'Mặc định'
        data['opt_btn_undo'] = 'Hoàn tác'
        data['opt_btn_close'] = 'Đóng'
        
        data['opt_msg_apply'] = 'Đã áp dụng tối ưu giao diện! Các khuyến cáo video vui lòng tự điều chỉnh.'
        data['opt_msg_undo'] = 'Đã khôi phục cài đặt trước khi tối ưu!'
        data['opt_msg_noundo'] = 'Không tìm thấy bản sao lưu nào!'
        data['opt_msg_default'] = 'Đã khôi phục cài đặt gốc của Tối ưu hoá!'
    else:
        data['opt_scan_sub'] = 'Checking CPU, RAM, Display, Battery and Network speed...'
        data['opt_specs'] = 'Smart Recommendations:'
        data['opt_spec_cpu'] = 'CPU'
        data['opt_spec_gpu'] = 'GPU'
        data['opt_spec_ram'] = 'RAM'
        data['opt_spec_screen'] = 'Screen'
        data['opt_spec_net'] = 'Network'
        data['opt_net_err'] = 'Network error'
        
        data['opt_high_end_title'] = 'Excellent!'
        data['opt_high_end_desc'] = 'Your system can easily handle 4K video and the most beautiful graphical settings.'
        
        data['opt_low_end_title'] = 'Modest Specs: '
        data['opt_low_end_desc'] = 'The system recommends disabling glass effects for the smoothest experience.'
        
        data['opt_std_title'] = 'Standard Specs: '
        data['opt_std_desc'] = 'Your computer is perfectly capable of playing 1080p video.'
        
        data['opt_bat_title'] = 'On Battery: '
        data['opt_bat_desc'] = 'To watch movies longer, prioritize 1080p and disable background effects to save power.'
        
        data['opt_fhd_title'] = 'Full HD Display: '
        data['opt_fhd_desc'] = 'Your screen cannot display 4K, so you should choose 1080p to avoid wasting CPU.'
        
        data['opt_net_title'] = 'Slow Network'
        data['opt_net_desc'] = 'You should change the default video quality to 720p or 1080p to avoid buffering.'
        
        data['opt_apply_title'] = 'Auto-apply UI settings (Check if desired):'
        data['opt_apply_min'] = 'Enable Minimalist UI (Disable 100% glassmorphism)'
        data['opt_apply_min_sub'] = 'Makes the app run super smooth on older computers.'
        data['opt_apply_amb'] = 'Disable Ambient Background'
        data['opt_apply_amb_sub1'] = 'Significantly reduces GPU load to save battery.'
        data['opt_apply_amb_sub2'] = 'Frees up graphical resources.'
        data['opt_apply_trl'] = 'Disable Auto-play Trailer'
        data['opt_apply_trl_sub1'] = 'Reduces disk and network usage to save battery.'
        data['opt_apply_trl_sub2'] = 'Reduces lag when opening a movie page.'
        data['opt_apply_all'] = 'Enable ALL graphical effects'
        data['opt_apply_all_sub'] = 'Your computer is strong enough to handle all heavy graphics.'
        data['opt_apply_note'] = 'Standard specs, you can tweak effects in Settings based on your preference.'
        
        data['opt_btn_default'] = 'Default'
        data['opt_btn_undo'] = 'Undo'
        data['opt_btn_close'] = 'Close'
        
        data['opt_msg_apply'] = 'Applied UI optimizations! Please adjust video recommendations manually.'
        data['opt_msg_undo'] = 'Restored settings prior to optimization!'
        data['opt_msg_noundo'] = 'No backup found!'
        data['opt_msg_default'] = 'Restored Optimizer to default settings!'

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch('assets/langs/vi.json')
patch('assets/langs/en.json')
