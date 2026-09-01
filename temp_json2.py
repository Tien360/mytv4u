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
  "translated_by_google": "Dịch tự động bởi Google Translate",
  "translating": "Đang dịch..."
}

en_keys = {
  "translated_by_google": "Translated by Google Translate",
  "translating": "Translating..."
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated JSON files")
