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
  "easter_spam_jokes_completed": [
    "Phim đã ra hết rồi, bạn định ép đạo diễn đẻ thêm tập à?",
    "Thơ tặng bạn:\n{MOVIE} kết thúc viên mãn\nXin đừng spam nữa, cho ngón tay nhàn!",
    "Bộ phim đã an nghỉ, xin đừng quấy rầy nó nữa!",
    "Bấm gì bấm nhiều thế? Tính đào mộ phim lên xem lại à?",
    "Người ta chiếu hết từ kiếp nào rồi mà còn đứng đây hóng tập mới!",
    "Thôi đừng bấm nữa, rụng nút bây giờ! Ra xem phim khác đi."
  ]
}

en_keys = {
  "easter_spam_jokes_completed": [
    "The movie is already finished. Do you want the director to spawn a new episode?",
    "A poem for you:\n{MOVIE} is done and gone\nStop spamming clicks and just move on!",
    "The series has rested in peace. Please don't disturb it!",
    "Why are you clicking? Trying to resurrect the movie?",
    "It finished airing ages ago, go watch something else!",
    "Stop clicking! You're gonna break the button!"
  ]
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated completed spam jokes JSON files")
