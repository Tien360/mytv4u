import json
import re
import os

vi_json_path = 'assets/langs/vi.json'
en_json_path = 'assets/langs/en.json'

with open(vi_json_path, 'r', encoding='utf-8') as f:
    vi_data = json.load(f)

with open(en_json_path, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

replacements = {
    # player_screen.dart
    'Máy chủ quá tải. Đang chuyển sang luồng dự phòng ({newDomain})...': ('server_overload', 'Máy chủ quá tải. Đang chuyển sang luồng dự phòng ({newDomain})...', 'Server overloaded. Switching to backup stream ({newDomain})...'),
    'Thông Báo Trình Phát': ('player_notice', 'Thông Báo Trình Phát', 'Player Notice'),
    'Phim chứa định dạng âm thanh Dolby TrueHD nhưng bản dựng mpv hiện tại chưa được tích hợp codec này.\\n\\n👉 Cách xử lý: Bấm vào nút Cài đặt (⚙️) -> Tab Âm thanh, và đổi sang một luồng âm thanh khác (như AC3 hoặc AAC) để có tiếng.': ('truehd_error', 'Phim chứa định dạng âm thanh Dolby TrueHD nhưng bản dựng mpv hiện tại chưa được tích hợp codec này.\\n\\n👉 Cách xử lý: Bấm vào nút Cài đặt (⚙️) -> Tab Âm thanh, và đổi sang một luồng âm thanh khác (như AC3 hoặc AAC) để có tiếng.', 'The video contains Dolby TrueHD audio, but the current mpv build lacks this codec.\\n\\n👉 Fix: Click Settings (⚙️) -> Audio tab, and switch to another audio stream (like AC3 or AAC).'),
    'Không thể tải dữ liệu Torrent.\\n\\nNguyên nhân: Link torrent này hiện không có đủ người chia sẻ (Seeders) hoặc bị lỗi kết nối mạng ngang hàng. Vui lòng thử chọn một server/chất lượng khác.': ('torrent_error', 'Không thể tải dữ liệu Torrent.\\n\\nNguyên nhân: Link torrent này hiện không có đủ người chia sẻ (Seeders) hoặc bị lỗi kết nối mạng ngang hàng. Vui lòng thử chọn một server/chất lượng khác.', 'Cannot load Torrent data.\\n\\nReason: This torrent lacks seeders or has network issues. Please try another server/quality.'),
    'Đã xảy ra lỗi:\\n{errorMsg}': ('generic_error', 'Đã xảy ra lỗi:\\n{errorMsg}', 'An error occurred:\\n{errorMsg}'),
    'Đóng thông báo': ('close_notice', 'Đóng thông báo', 'Close notice'),
    'Bộ lọc màu Video': ('video_color_filter', 'Bộ lọc màu Video', 'Video Color Filter'),
    'Tốc độ phát': ('playback_speed', 'Tốc độ phát', 'Playback Speed'),
    '1x (Chuẩn)': ('speed_normal', '1x (Chuẩn)', '1x (Normal)'),
    'Tự động chuyển tập': ('auto_next_ep', 'Tự động chuyển tập', 'Auto Next Episode'),
    'Tăng tốc phần cứng (HW Accel)': ('hw_accel', 'Tăng tốc phần cứng (HW Accel)', 'Hardware Acceleration (HW Accel)'),
    'Tắt nếu gặp lỗi màn hình đen': ('hw_accel_desc', 'Tắt nếu gặp lỗi màn hình đen', 'Turn off if you see a black screen'),
    'Đồng bộ Âm thanh': ('sync_audio', 'Đồng bộ Âm thanh', 'Audio Sync'),
    'Đồng bộ Phụ đề': ('sync_subtitle', 'Đồng bộ Phụ đề', 'Subtitle Sync'),
    'Thêm tệp âm thanh rời...': ('add_external_audio', 'Thêm tệp âm thanh rời...', 'Add external audio file...'),
    'Thêm tệp phụ đề rời...': ('add_external_sub', 'Thêm tệp phụ đề rời...', 'Add external subtitle file...'),
    'Chung': ('tab_general', 'Chung', 'General'),
    'Âm thanh': ('tab_audio', 'Âm thanh', 'Audio'),
    'Phụ đề chính': ('tab_sub_main', 'Phụ đề chính', 'Main Subtitle'),
    'Phụ đề phụ': ('tab_sub_sec', 'Phụ đề phụ', 'Secondary Subtitle'),
    'Thông tin': ('tab_info', 'Thông tin', 'Info'),
    'Đang chọn: ': ('currently_selected', 'Đang chọn: ', 'Selected: '),
    'Tự động': ('auto', 'Tự động', 'Auto'),
    'Tắt': ('off', 'Tắt', 'Off'),
    'Chuyển Tập Ngay': ('next_ep_now', 'Chuyển Tập Ngay', 'Next Ep Now'),
    'Đóng': ('close', 'Đóng', 'Close'),
    
    # tv_screen.dart & widgets
    'Tải thêm': ('load_more', 'Tải thêm', 'Load More'),
    'Trang chủ': ('home', 'Trang chủ', 'Home'),
    'Nổi Bật': ('featured', 'Nổi Bật', 'Featured'),
    'Phim Lẻ': ('movies', 'Phim Lẻ', 'Movies'),
    'Phim Bộ': ('tv_shows', 'Phim Bộ', 'TV Shows'),
    'Hoạt Hình': ('anime', 'Hoạt Hình', 'Anime'),
    'TV Shows': ('tv_shows_vi', 'TV Shows', 'TV Shows'),
    'Làm mới': ('refresh', 'Làm mới', 'Refresh'),
    
    # actor_detail_screen.dart
    'Chưa có thông tin tiểu sử.': ('no_bio', 'Chưa có thông tin tiểu sử.', 'No biography available.'),
    'Tiểu sử': ('biography', 'Tiểu sử', 'Biography'),
    'Phim đã tham gia': ('movies_participated', 'Phim đã tham gia', 'Movies participated'),
    'Phim tham gia': ('movies_participated_short', 'Phim tham gia', 'Movies'),
    
    # splash_screen.dart
    'Đang khởi tạo ứng dụng...': ('initializing_app', 'Đang khởi tạo ứng dụng...', 'Initializing app...'),
    'Khởi tạo thất bại!': ('init_failed', 'Khởi tạo thất bại!', 'Initialization failed!'),
    
    # global_color_settings.dart & advanced_controls_panel.dart
    'Điều chỉnh': ('adjust', 'Điều chỉnh', 'Adjust'),
    'Màu sắc Video': ('video_color', 'Màu sắc Video', 'Video Color'),
    'Mặc định': ('default', 'Mặc định', 'Default'),
    'Sống động': ('vivid', 'Sống động', 'Vivid'),
    'Rạp phim': ('cinema', 'Rạp phim', 'Cinema'),
    'Sáng rực': ('bright', 'Sáng rực', 'Bright'),
    'Đen trắng': ('bw', 'Đen trắng', 'B&W'),
    'Ấm áp': ('warm', 'Ấm áp', 'Warm'),
    'Lạnh': ('cool', 'Lạnh', 'Cool'),
    'Tùy chỉnh': ('custom', 'Tùy chỉnh', 'Custom'),
    'Bộ lọc:': ('filter_label', 'Bộ lọc:', 'Filter:'),
    'Độ sáng': ('brightness', 'Độ sáng', 'Brightness'),
    'Tương phản': ('contrast', 'Tương phản', 'Contrast'),
    'Độ bão hòa màu': ('saturation', 'Độ bão hòa màu', 'Saturation'),
    'Chỉnh độ trễ hiển thị phụ đề so với video. Số âm (-) nghĩa là phụ đề hiện sớm hơn.': ('sub_delay_desc', 'Chỉnh độ trễ hiển thị phụ đề so với video. Số âm (-) nghĩa là phụ đề hiện sớm hơn.', 'Adjust subtitle delay. Negative (-) means subtitle appears earlier.'),
    'Chỉnh độ trễ âm thanh so với video. Số âm (-) nghĩa là âm thanh phát sớm hơn.': ('audio_delay_desc', 'Chỉnh độ trễ âm thanh so với video. Số âm (-) nghĩa là âm thanh phát sớm hơn.', 'Adjust audio delay. Negative (-) means audio plays earlier.'),
    'Độ trễ (ms)': ('delay_ms', 'Độ trễ (ms)', 'Delay (ms)'),
    'Mặc định (0 ms)': ('default_0ms', 'Mặc định (0 ms)', 'Default (0 ms)'),
    
    # update_dialog.dart
    'Có phiên bản mới: ': ('new_version_available', 'Có phiên bản mới: ', 'New version available: '),
    'Cập nhật ngay': ('update_now', 'Cập nhật ngay', 'Update now'),
    'Để sau': ('later', 'Để sau', 'Later'),
}

for r_key, (json_key, vi_val, en_val) in replacements.items():
    vi_data[json_key] = vi_val
    en_data[json_key] = en_val

with open(vi_json_path, 'w', encoding='utf-8') as f:
    json.dump(vi_data, f, ensure_ascii=False, indent=2)

with open(en_json_path, 'w', encoding='utf-8') as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)

print("Updated JSON files")
