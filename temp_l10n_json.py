import json

def add_key(file_path, key, val):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return
    if key not in data:
        data[key] = val
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

add_key("assets/langs/vi.json", "nav_gaming", "Trò chơi")
add_key("assets/langs/vi.json", "game_webview_player", "Trình phát Game WebView")

add_key("assets/langs/en.json", "nav_gaming", "Gaming")
add_key("assets/langs/en.json", "game_webview_player", "Game WebView Player")

print("Updated l10n JSONs")
