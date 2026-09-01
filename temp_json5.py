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
  "ep_msg_previous_missing": [
    "App bị hổng mất tập {LAST_EP} rồi. Tức á!",
    "Nguồn phim ăn bớt tập {LAST_EP} rồi! Đang chờ admin cập nhật."
  ],
  "ep_msg_vip_ahead": [
    "Tập {X} đã chiếu bên VIP nhưng nguồn free chưa tuồn ra kịp.",
    "Đang đợi nguồn mót tập {X} từ bản VIP của nhà đài."
  ],
  "ep_msg_today_finale_available": [
    "ĐẠI TỰU! Tập {X} (Cuối) ĐÃ LÊN SÓNG!",
    "Trùm cuối {X} đây rồi! Luyện ngay cho nóng!"
  ],
  "ep_msg_today_finale_unavailable": [
    "Tập Cuối {X} ra lò hôm nay rồi, nguồn phim đang xào nấu, hóng quá!",
    "Ngày tàn của bộ phim tới rồi (Tập {X}), F5 liên tục nào!"
  ],
  "ep_msg_today_unavailable": [
    "Tập {X} chiếu hôm nay mà nguồn phim chưa có hàng!",
    "Nhà đài vừa chiếu tập {X}, nguồn lậu đang hì hục reup, ráng đợi nghen!"
  ],
  "ep_msg_tomorrow": [
    "Ngày mai là có tập {X} rồi! Ngủ sớm lấy sức thôi.",
    "Chỉ còn 1 lần chớp mắt nữa là tới tập {X}!"
  ]
}

en_keys = {
  "ep_msg_previous_missing": [
    "Episode {LAST_EP} is missing from the source! Grrr!",
    "Source skipped episode {LAST_EP}. Waiting for an update."
  ],
  "ep_msg_vip_ahead": [
    "Episode {X} is out for VIPs, waiting for free release.",
    "Hunting down episode {X} from VIP sources..."
  ],
  "ep_msg_today_finale_available": [
    "IT'S HERE! The Finale (Ep {X}) is available!",
    "The final boss (Ep {X}) has arrived! Watch it now!"
  ],
  "ep_msg_today_finale_unavailable": [
    "Finale (Ep {X}) airs today! Source is still preparing it.",
    "The end is near! Waiting for the source to upload Ep {X}."
  ],
  "ep_msg_today_unavailable": [
    "Episode {X} airs today, but the source hasn't uploaded it yet!",
    "Awaiting Ep {X} upload... refresh soon!"
  ],
  "ep_msg_tomorrow": [
    "Episode {X} drops tomorrow! Get some sleep.",
    "Just one more sleep until episode {X}!"
  ]
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated JSON files")
