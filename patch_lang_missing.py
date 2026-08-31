import json

with open('assets/langs/vi.json', 'r', encoding='utf-8') as f:
    vi = json.load(f)

vi['ep_msg_previous_missing'] = [
    "Tập {LAST_EP} chiếu từ đời nào rồi mà chưa thấy vietsub đâu, đợi mòn cả dép!",
    "TMDB báo sắp chiếu tập {X} mà app mình vẫn chưa kiếm ra vietsub tập {LAST_EP}. Hóng team sub cứu giá!",
    "Tập {LAST_EP} đã lên sóng nhưng chưa có hàng, bạn chịu khó đợi thêm chút xíu nhé!"
]

with open('assets/langs/vi.json', 'w', encoding='utf-8') as f:
    json.dump(vi, f, ensure_ascii=False, indent=2)

with open('assets/langs/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

en['ep_msg_previous_missing'] = [
    "Episode {LAST_EP} already aired but we haven't found the subtitles yet. Hang tight!",
    "TMDB says Episode {X} is coming, but we're still waiting for Episode {LAST_EP}'s subs!",
    "Episode {LAST_EP} is missing from our sources. Please wait a little longer!"
]

with open('assets/langs/en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print("Added ep_msg_previous_missing to language files")
