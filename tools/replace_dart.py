import os

replacements = {
    # player_screen.dart
    "'Máy chủ quá tải. Đang chuyển sang luồng dự phòng ()...'": "L10n.t('server_overload', {'newDomain': newDomain})",
    "'Thông Báo Trình Phát'": "L10n.t('player_notice')",
    "'Phim chứa định dạng âm thanh Dolby TrueHD nhưng bản dựng mpv hiện tại chưa được tích hợp codec này.\\n\\n👉 Cách xử lý: Bấm vào nút Cài đặt (⚙️) -> Tab Âm thanh, và đổi sang một luồng âm thanh khác (như AC3 hoặc AAC) để có tiếng.'": "L10n.t('truehd_error')",
    "'Không thể tải dữ liệu Torrent.\\n\\nNguyên nhân: Link torrent này hiện không có đủ người chia sẻ (Seeders) hoặc bị lỗi kết nối mạng ngang hàng. Vui lòng thử chọn một server/chất lượng khác.'": "L10n.t('torrent_error')",
    "'Đã xảy ra lỗi:\\n'": "L10n.t('generic_error', {'errorMsg': errorMsg!})",
    "'Đóng thông báo'": "L10n.t('close_notice')",
    "'Bộ lọc màu Video'": "L10n.t('video_color_filter')",
    "'Tốc độ phát'": "L10n.t('playback_speed')",
    "'1x (Chuẩn)'": "L10n.t('speed_normal')",
    "'Tự động chuyển tập'": "L10n.t('auto_next_ep')",
    "'Tăng tốc phần cứng (HW Accel)'": "L10n.t('hw_accel')",
    "'Tắt nếu gặp lỗi màn hình đen'": "L10n.t('hw_accel_desc')",
    "'Đồng bộ Âm thanh'": "L10n.t('sync_audio')",
    "'Đồng bộ Phụ đề'": "L10n.t('sync_subtitle')",
    "'Thêm tệp âm thanh rời...'": "L10n.t('add_external_audio')",
    "'Thêm tệp phụ đề rời...'": "L10n.t('add_external_sub')",
    "'Chung'": "L10n.t('tab_general')",
    "'Âm thanh'": "L10n.t('tab_audio')",
    "'Phụ đề chính'": "L10n.t('tab_sub_main')",
    "'Phụ đề phụ'": "L10n.t('tab_sub_sec')",
    "'Thông tin'": "L10n.t('tab_info')",
    "'Đang chọn: '": "L10n.t('currently_selected')",
    "'Tự động'": "L10n.t('auto')",
    "'Tắt'": "L10n.t('off')",
    "'Chuyển Tập Ngay'": "L10n.t('next_ep_now')",
    "'Đóng'": "L10n.t('close')",
    
    # tv_screen.dart & widgets
    "'Tải thêm'": "L10n.t('load_more')",
    "'Trang chủ'": "L10n.t('home')",
    "'Nổi Bật'": "L10n.t('featured')",
    "'Phim Lẻ'": "L10n.t('movies')",
    "'Phim Bộ'": "L10n.t('tv_shows')",
    "'Hoạt Hình'": "L10n.t('anime')",
    "'TV Shows'": "L10n.t('tv_shows_vi')",
    "'Làm mới'": "L10n.t('refresh')",
    
    # actor_detail_screen.dart
    "'Chưa có thông tin tiểu sử.'": "L10n.t('no_bio')",
    "'Tiểu sử'": "L10n.t('biography')",
    "'Phim đã tham gia'": "L10n.t('movies_participated')",
    "'Phim tham gia'": "L10n.t('movies_participated_short')",
    
    # splash_screen.dart
    "'Đang khởi tạo ứng dụng...'": "L10n.t('initializing_app')",
    "'Khởi tạo thất bại!'": "L10n.t('init_failed')",
    
    # widgets
    "'Điều chỉnh'": "L10n.t('adjust')",
    "'Màu sắc Video'": "L10n.t('video_color')",
    "'Mặc định'": "L10n.t('default')",
    "'Sống động'": "L10n.t('vivid')",
    "'Rạp phim'": "L10n.t('cinema')",
    "'Sáng rực'": "L10n.t('bright')",
    "'Đen trắng'": "L10n.t('bw')",
    "'Ấm áp'": "L10n.t('warm')",
    "'Lạnh'": "L10n.t('cool')",
    "'Tùy chỉnh'": "L10n.t('custom')",
    "'Bộ lọc:'": "L10n.t('filter_label')",
    "'Độ sáng'": "L10n.t('brightness')",
    "'Tương phản'": "L10n.t('contrast')",
    "'Độ bão hòa màu'": "L10n.t('saturation')",
    "'Chỉnh độ trễ hiển thị phụ đề so với video. Số âm (-) nghĩa là phụ đề hiện sớm hơn.'": "L10n.t('sub_delay_desc')",
    "'Chỉnh độ trễ âm thanh so với video. Số âm (-) nghĩa là âm thanh phát sớm hơn.'": "L10n.t('audio_delay_desc')",
    "'Độ trễ (ms)'": "L10n.t('delay_ms')",
    "'Mặc định (0 ms)'": "L10n.t('default_0ms')",
    
    # update_dialog.dart
    "'Có phiên bản mới: '": "L10n.t('new_version_available')",
    "'Cập nhật ngay'": "L10n.t('update_now')",
    "'Để sau'": "L10n.t('later')",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old_str, new_str in replacements.items():
        new_content = new_content.replace(old_str, new_str)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('lib'):
    for file in files:
        if file.endswith('.dart'):
            process_file(os.path.join(root, file))

