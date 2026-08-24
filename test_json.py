import json
with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
        print("Valid JSON. trailer_stop:", data.get("trailer_stop"))
    except Exception as e:
        print("JSON Error:", e)
