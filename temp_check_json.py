import json
try:
    with open('assets/langs/en.json', 'r', encoding='utf-8') as f:
        json.load(f)
    print("en.json is valid!")
except Exception as e:
    print("en.json is INVALID:", e)
