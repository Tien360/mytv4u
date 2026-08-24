import json

files = ["assets/langs/vi.json", "assets/langs/en.json"]
translations = {
    "vi": {
        "trailer_search": "Tìm Trailer",
        "trailer_stop": "Dừng Trailer",
        "trailer_replay": "Phát lại Trailer",
        "trailer_play": "Phát Trailer"
    },
    "en": {
        "trailer_search": "Search Trailer",
        "trailer_stop": "Stop Trailer",
        "trailer_replay": "Replay Trailer",
        "trailer_play": "Play Trailer"
    }
}

for file in files:
    lang = "vi" if "vi" in file else "en"
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for k, v in translations[lang].items():
        data[k] = v
        
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
print("Updated json files.")
