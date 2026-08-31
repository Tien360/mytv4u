import json

with open('assets/langs/vi.json', 'r', encoding='utf-8') as f:
    vi = json.load(f)

vi['ep_msg_tomorrow'] = [
    "Ngày mai ({DATE}) là có tập {X} rồi, chuẩn bị tinh thần hóng thôi!",
    "Chỉ còn 1 ngày nữa là tập {X} lên sóng ({DATE}). Cố lên sắp được xem rồi!",
    "Tập {X} sẽ hạ cánh vào ngày mai ({DATE}). Đặt lịch nhắc nhở ngay đi nào!"
]

with open('assets/langs/vi.json', 'w', encoding='utf-8') as f:
    json.dump(vi, f, ensure_ascii=False, indent=2)

with open('assets/langs/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

en['ep_msg_tomorrow'] = [
    "Tomorrow ({DATE}) is the day for Episode {X}. Get ready!",
    "Just 1 day left until Episode {X} airs ({DATE}). Hang in there!",
    "Episode {X} drops tomorrow ({DATE}). Set your alarms!"
]

with open('assets/langs/en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print("Added ep_msg_tomorrow to language files")
