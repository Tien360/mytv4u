import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

replace_in_file('lib/screens/movie_detail_screen.dart', [
    ("'Đăng nhập để bình luận...'", "L10n.t('login_to_comment') ?? 'Đăng nhập để bình luận...'"),
    ("'Viết bình luận của bạn...'", "L10n.t('write_your_comment') ?? 'Viết bình luận của bạn...'"),
    ("'Đăng nhập & Gửi'", "L10n.t('login_and_send') ?? 'Đăng nhập & Gửi'"),
    ("'Gửi bình luận'", "L10n.t('send_comment') ?? 'Gửi bình luận'"),
    ("'Chưa có bình luận nào.'", "L10n.t('no_comments_yet') ?? 'Chưa có bình luận nào.'"),
    ("'Xem thêm bình luận'", "L10n.t('view_more_comments') ?? 'Xem thêm bình luận'")
])

replace_in_file('lib/widgets/global_color_settings.dart', [
    ("'Video chạy mẫu:'", "L10n.t('sample_video') ?? 'Video chạy mẫu:'"),
    ("'Bộ lọc có sẵn:'", "L10n.t('available_filters') ?? 'Bộ lọc có sẵn:'")
])

print("Replaced in movie_detail_screen.dart and global_color_settings.dart")
