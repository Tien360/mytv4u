import json

def update_json(file_path, new_keys):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in new_keys.items():
        if k not in data:
            data[k] = v
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

vi_keys = {
  "error_tmdb_id_not_found": "Không tìm thấy ID TMDB",
  "error_no_seasons": "Không có thông tin các Phần (Seasons).",
  "error_no_valid_seasons": "Phim chưa có phần nào hợp lệ.",
  "error_prefix": "Lỗi",
  "error_loading_episodes": "Lỗi tải tập phim",
  "season": "Phần",
  "episode": "Tập",
  "released": "Đã chiếu",
  "upcoming": "Sắp chiếu",
  "minutes": "phút",
  "votes": "đánh giá",
  "director": "Đạo diễn",
  "writer": "Biên kịch",
  "guest_stars": "Diễn viên khách mời",
  "air_schedule": "Cẩm nang Tập phim",
  "no_schedule_found": "Chưa có thông tin lịch chiếu từ TMDB."
}

en_keys = {
  "error_tmdb_id_not_found": "TMDB ID not found",
  "error_no_seasons": "No seasons information available.",
  "error_no_valid_seasons": "No valid seasons available.",
  "error_prefix": "Error",
  "error_loading_episodes": "Error loading episodes",
  "season": "Season",
  "episode": "Episode",
  "released": "Released",
  "upcoming": "Upcoming",
  "minutes": "mins",
  "votes": "votes",
  "director": "Director",
  "writer": "Writer",
  "guest_stars": "Guest Stars",
  "air_schedule": "Air Schedule",
  "no_schedule_found": "No air schedule information from TMDB."
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated JSON files")
