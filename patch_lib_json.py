import json

def update_lang(path, new_keys):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.update(new_keys)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

vi_keys = {
  "open_link": "Mở Link",
  "open_file": "Mở File",
  "open_url_title": "Mở đường dẫn mạng (URL)",
  "open_url_hint": "Nhập link video/audio (mp4, m3u8, mp3...)",
  "mark_as_live": "Đánh dấu là luồng trực tiếp (Live)",
  "cancel": "Hủy",
  "network_stream": "Luồng Mạng",
  "loading_mix_playlist": "Đang tải danh sách Mix/Playlist...",
  "open": "Mở",
  "library_title": "Thư viện & Yêu thích"
}

en_keys = {
  "open_link": "Open Link",
  "open_file": "Open File",
  "open_url_title": "Open Network Stream (URL)",
  "open_url_hint": "Enter video/audio link (mp4, m3u8, mp3...)",
  "mark_as_live": "Mark as live stream",
  "cancel": "Cancel",
  "network_stream": "Network Stream",
  "loading_mix_playlist": "Loading Mix/Playlist...",
  "open": "Open",
  "library_title": "Library & Favorites"
}

update_lang("assets/langs/vi.json", vi_keys)
update_lang("assets/langs/en.json", en_keys)
print("Updated library_screen keys")
