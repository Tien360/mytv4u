import json

with open("assets/langs/vi.json","r",encoding="utf-8") as f: vi = json.load(f)
with open("assets/langs/en.json","r",encoding="utf-8") as f: en = json.load(f)

vi["easter_eggs_title"] = "Hieu ung Tuong tac (Easter Eggs)"
vi["easter_eggs_toggle"] = "Bat Hieu ung Trung Phuc Sinh"
vi["easter_eggs_desc"] = "Nhan vao dong trang thai tap moi o moi phim de quay thuong hieu ung! Co 4 bac tu Pho thong den Huyen thoai (ti le 1%). Chuc ban may man!"

en["easter_eggs_title"] = "Interactive Effects (Easter Eggs)"
en["easter_eggs_toggle"] = "Enable Easter Egg Effects"
en["easter_eggs_desc"] = "Tap the episode status line on any movie to spin for effects! 4 tiers from Common to Legendary (1% chance). Good luck!"

with open("assets/langs/vi.json","w",encoding="utf-8") as f: json.dump(vi, f, ensure_ascii=False, indent=2)
with open("assets/langs/en.json","w",encoding="utf-8") as f: json.dump(en, f, ensure_ascii=False, indent=2)
print("L10n keys added!")
