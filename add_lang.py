import json

def add_keys(path, new_keys):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.update(new_keys)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_keys("assets/langs/vi.json", {
    "ambient_bg": "Ambient Background",
    "ambient_bg_desc": "Hiển thị hình nền mờ từ poster phim giúp giao diện sống động hơn"
})

add_keys("assets/langs/en.json", {
    "ambient_bg": "Ambient Background",
    "ambient_bg_desc": "Display a blurred background from the movie poster for a more dynamic interface"
})

print("Keys added to JSON files.")
