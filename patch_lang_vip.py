import json

with open('assets/langs/vi.json', 'r', encoding='utf-8') as f:
    vi = json.load(f)

vi['ep_msg_vip_ahead'] = [
    "Nguồn phim VIP đã cập nhật đến tập {MAX_EP}, vượt luôn cả lịch chiếu chính thức! Cháy quá!",
    "TMDB báo hôm nay mới chiếu tập {X}, nhưng app mình đã có đến tập {MAX_EP} rồi nhé. Cày thôi!",
    "Lịch chiếu chính thức mới tới tập {X}, mà nguồn phim đã đi trước thời đại đến tập {MAX_EP} luôn rồi!"
]

with open('assets/langs/vi.json', 'w', encoding='utf-8') as f:
    json.dump(vi, f, ensure_ascii=False, indent=2)

with open('assets/langs/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

en['ep_msg_vip_ahead'] = [
    "VIP sources already have up to Episode {MAX_EP}, ahead of the official schedule! Let's go!",
    "TMDB says Episode {X} is next, but we already have Episode {MAX_EP}. Enjoy the early access!",
    "Official schedule is at Episode {X}, but we are living in the future with Episode {MAX_EP}!"
]

with open('assets/langs/en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print("Added ep_msg_vip_ahead to language files")
