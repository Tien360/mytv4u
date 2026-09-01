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
  "easter_spam_jokes": [
    "Bấm gì bấm nhiều thế? Bộ tính làm hacker hở?",
    "Bạn có spam cháy cả chuột thì phim cũng chưa ra tập mới đâu!",
    "Thơ tặng bạn:\n{MOVIE} hay thật là hay\nNhưng mà chưa chiếu, bấm hoài đứt tay!",
    "Tôi là hộp báo lịch, không phải máy đẻ tập phim mới nha!",
    "Đã bảo là chưa có mà! Lì xì admin 50k đi rồi tôi giục đạo diễn cho.",
    "Hết văn để trêu bạn rồi! Mỏi tay chưa? Tắt máy đi ngủ đi!",
    "Bạn bấm nát cái nút rồi kìa. Lạy chúa tôi!",
    "Nếu bạn bấm thêm 100 lần nữa, tập mới sẽ... vẫn không xuất hiện =))",
    "Thơ về phim:\n{MOVIE} kịch tính bất ngờ\nSpam hoài đau ngón, thẫn thờ chờ mong!",
    "Nghịch hoài không chán hả bạn gì ơi?",
    "Nhấp chuột 10 lần 1 giây... bạn chơi game MOBA chắc pro lắm nhỉ?",
    "Đã bảo là không có gì đâu mà cứ bấm! Ngoan, đi xem phim khác đi."
  ]
}

en_keys = {
  "easter_spam_jokes": [
    "Why so many clicks? Are you trying to hack the matrix?",
    "Spamming the button won't make the episode render faster!",
    "A poem for you:\n{MOVIE} is great, it's true\nBut clicking won't bring it to you!",
    "I'm a calendar, not an episode generator!",
    "I told you it's not out yet! Bribe the admin and maybe we'll talk.",
    "I ran out of jokes. Are your fingers tired? Go to sleep!",
    "You're breaking the button! Good lord!",
    "If you click 100 more times, the new episode will... still not be here.",
    "A haiku for {MOVIE}:\nWaiting is so hard\nYou click the button again\nNothing happens here.",
    "Aren't you bored of clicking yet?",
    "10 clicks per second... you must be a pro gamer.",
    "Stop clicking! Be a good viewer and watch something else."
  ]
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated JSON files")
