path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "'Thư viện & Yêu thích'": "L10n.t('library_title')",
    "'Mở Link'": "L10n.t('open_link')",
    "'Mở File'": "L10n.t('open_file')",
    "'Mở đường dẫn mạng (URL)'": "L10n.t('open_url_title')",
    "'Nhập link video/audio (mp4, m3u8, mp3...)'": "L10n.t('open_url_hint')",
    "'Đánh dấu là luồng trực tiếp (Live)'": "L10n.t('mark_as_live')",
    "Text('Hủy'": "Text(L10n.t('cancel')",
    "'Luồng Mạng'": "L10n.t('network_stream')",
    "'Đang tải danh sách Mix/Playlist...'": "L10n.t('loading_mix_playlist')",
    "Text('Mở'": "Text(L10n.t('open')"
}

for k, v in replacements.items():
    content = content.replace(k, v)

# Also remove const if there are any Text(L10n.t)
content = content.replace("const Text(L10n.t", "Text(L10n.t")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated library_screen strings")
