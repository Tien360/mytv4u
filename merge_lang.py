import json

with open("vi_easter.json","r",encoding="utf-8-sig") as f: vi_e = json.load(f)
with open("en_easter.json","r",encoding="utf-8-sig") as f: en_e = json.load(f)
with open("assets/langs/vi.json","r",encoding="utf-8") as f: vi = json.load(f)
with open("assets/langs/en.json","r",encoding="utf-8") as f: en = json.load(f)

vi.update(vi_e)
en.update(en_e)

with open("assets/langs/vi.json","w",encoding="utf-8") as f: json.dump(vi, f, ensure_ascii=False, indent=2)
with open("assets/langs/en.json","w",encoding="utf-8") as f: json.dump(en, f, ensure_ascii=False, indent=2)
print("Done!")
