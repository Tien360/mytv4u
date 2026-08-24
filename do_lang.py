import json

with open("assets/langs/en.json", "r", encoding="utf-8") as f:
    en = json.load(f)

en['overview'] = "Overview"
en['next_episode'] = "Next episode: "

with open("assets/langs/en.json", "w", encoding="utf-8") as f:
    json.dump(en, f, indent=2, ensure_ascii=False)

with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    vi = json.load(f)

vi['overview'] = "Nội dung phim"
vi['next_episode'] = "Tập tiếp theo: "

with open("assets/langs/vi.json", "w", encoding="utf-8") as f:
    json.dump(vi, f, indent=2, ensure_ascii=False)

print("Updated translation files!")
