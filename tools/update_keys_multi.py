import json
import re
import sys

def update_langs(additions):
    for lang, items in additions.items():
        filepath = f'assets/langs/{lang}.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for k, v in items.items():
            data[k] = v
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

vi = {
    'login_to_comment': 'Đăng nhập để bình luận...',
    'write_your_comment': 'Viết bình luận của bạn...',
    'login_and_send': 'Đăng nhập & Gửi',
    'send_comment': 'Gửi bình luận',
    'no_comments_yet': 'Chưa có bình luận nào.',
    'view_more_comments': 'Xem thêm bình luận',
    'sample_video': 'Video chạy mẫu:',
    'available_filters': 'Bộ lọc có sẵn:',
    'ep_name': 'Tập {name}',
    'from_beginning': 'Từ đầu',
    'resume_playing': 'Xem tiếp',
    'resume_prompt': 'Bạn đã xem đến {time}. Bạn muốn xem tiếp hay xem lại từ đầu?',
    'unknown': 'Không rõ',
    'auto_default': 'Tự động (Mặc định)',
    'stream_id': 'Luồng {id}',
    'next_ep_in': 'Tập tiếp theo sẽ phát sau {time} giây',
    'closing_in': 'Phim sẽ đóng sau {time} giây',
    'finished': 'Kết thúc',
    'selecting_track': 'Đang chọn: {track}',
    'movie_title': 'Tên phim',
    'current_ep': 'Tập đang phát',
    'duration': 'Thời lượng',
    'resolution': 'Độ phân giải',
    'streaming_source': 'Nguồn phát',
    'web_browser_embed': 'Trình duyệt Web (Embed)',
    'native_video_player': 'Trình phát Video gốc',
    'sub_source': 'Nguồn phụ:',
    'opening_high_res': 'Đang mở trình phát độ phân giải cao...\n(Bấm ESC bên cửa sổ kia để thoát)',
    'go_back': 'Quay lại',
    'pause_space': 'Tạm dừng (Space)',
    'play_space': 'Phát (Space)',
    'rewind_10s': 'Lùi 10s (←)',
    'forward_10s': 'Tới 10s (→)',
    'volume': 'Âm lượng',
    'next_episode': 'Tập tiếp theo',
    'ep_list': 'Danh sách tập',
    'fullscreen': 'Toàn màn hình',
    'select_episode': 'Chọn tập'
}

en = {
    'login_to_comment': 'Login to comment...',
    'write_your_comment': 'Write your comment...',
    'login_and_send': 'Login & Send',
    'send_comment': 'Send comment',
    'no_comments_yet': 'No comments yet.',
    'view_more_comments': 'View more comments',
    'sample_video': 'Sample video:',
    'available_filters': 'Available filters:',
    'ep_name': 'Episode {name}',
    'from_beginning': 'From start',
    'resume_playing': 'Resume',
    'resume_prompt': 'You stopped at {time}. Resume playing or start from the beginning?',
    'unknown': 'Unknown',
    'auto_default': 'Auto (Default)',
    'stream_id': 'Stream {id}',
    'next_ep_in': 'Next episode in {time}s',
    'closing_in': 'Closing in {time}s',
    'finished': 'Finished',
    'selecting_track': 'Selecting: {track}',
    'movie_title': 'Title',
    'current_ep': 'Current episode',
    'duration': 'Duration',
    'resolution': 'Resolution',
    'streaming_source': 'Source',
    'web_browser_embed': 'Web Browser (Embed)',
    'native_video_player': 'Native Video Player',
    'sub_source': 'Sub-source:',
    'opening_high_res': 'Opening high-res player...\n(Press ESC on the other window to exit)',
    'go_back': 'Go back',
    'pause_space': 'Pause (Space)',
    'play_space': 'Play (Space)',
    'rewind_10s': 'Rewind 10s (←)',
    'forward_10s': 'Forward 10s (→)',
    'volume': 'Volume',
    'next_episode': 'Next episode',
    'ep_list': 'Episodes list',
    'fullscreen': 'Fullscreen',
    'select_episode': 'Select episode'
}

update_langs({'vi': vi, 'en': en})
print("Added keys to JSON")
