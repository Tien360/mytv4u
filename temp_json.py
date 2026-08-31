import json

def update_json(filepath, updates):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.update(updates)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json("assets/langs/en.json", {
    "air_schedule": "Air Schedule",
    "no_schedule_found": "No TMDB schedule info found.",
    "air_date": "Air Date"
})

update_json("assets/langs/vi.json", {
    "air_schedule": "Lịch phát sóng",
    "no_schedule_found": "Chưa có thông tin lịch chiếu từ TMDB.",
    "air_date": "Ngày chiếu"
})
print("Updated JSON files")
