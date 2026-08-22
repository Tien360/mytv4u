import json
import re
files = ['assets/langs/en.json', 'assets/langs/vi.json']
new_keys = {
    'en.json': {
        'all': 'All',
        'tv_channels_title': 'Live TV Channels',
        'tv_channels_subtitle': 'Watch VTV, HTV, VTC, and local channels live in high quality',
        'no_tv_channels': 'No TV channels found',
        'tv360_webview_player': 'TV360 Live WebView Player',
        'reload_page': 'Reload page',
        'webview_load_error': 'Failed to load WebView: {error}',
        'opening_tv360_web_player': 'Opening TV360 Web Player in app...'
    },
    'vi.json': {
        'all': 'Tất cả',
        'tv_channels_title': 'Kênh Truyền Hình TV Trực Tuyến',
        'tv_channels_subtitle': 'Xem trực tiếp các kênh VTV, HTV, VTC, Truyền hình tỉnh chất lượng cao',
        'no_tv_channels': 'Không tìm thấy kênh truyền hình nào',
        'tv360_webview_player': 'Trình phát WebView TV360 Trực tiếp',
        'reload_page': 'Tải lại trang',
        'webview_load_error': 'Không thể tải WebView: {error}',
        'opening_tv360_web_player': 'Đang mở TV360 Web Player trong ứng dụng...'
    }
}
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    filename = file.split('/')[-1]
    for k, v in new_keys[filename].items():
        if k not in data:
            data[k] = v
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

with open('lib/screens/tv_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'Tất cả'", "L10n.t('all') ?? 'Tất cả'")
content = content.replace("'Kênh Truyền Hình TV Trực Tuyến'", "L10n.t('tv_channels_title') ?? 'Kênh Truyền Hình TV Trực Tuyến'")
content = content.replace("'Xem trực tiếp các kênh VTV, HTV, VTC, Truyền hình tỉnh chất lượng cao'", "L10n.t('tv_channels_subtitle') ?? 'Xem trực tiếp các kênh...'")
content = content.replace("'Không tìm thấy kênh truyền hình nào'", "L10n.t('no_tv_channels') ?? 'Không tìm thấy kênh truyền hình nào'")

with open('lib/screens/tv_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

with open('lib/screens/tv_webview_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
    
content = content.replace("'Trình phát WebView TV360 Trực tiếp'", "L10n.t('tv360_webview_player') ?? 'Trình phát WebView TV360'")
content = content.replace("'Tải lại trang'", "L10n.t('reload_page') ?? 'Tải lại trang'")
content = content.replace("'Không thể tải WebView: $_error'", "L10n.t('webview_load_error', {'error': _error}) ?? 'Lỗi tải'")
content = content.replace("'Đang mở TV360 Web Player trong ứng dụng...'", "L10n.t('opening_tv360_web_player') ?? 'Đang mở TV360'")

with open('lib/screens/tv_webview_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done tv screens')
