import json

def update_json(file_path, new_keys):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in new_keys.items():
        if k not in data:
            data[k] = v
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json("assets/langs/vi.json", {"this_movie": "Bộ phim này"})
update_json("assets/langs/en.json", {"this_movie": "This movie"})
print("Updated this_movie key")
