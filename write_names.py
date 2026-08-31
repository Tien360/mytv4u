import json
with open('missing.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)
with open('missing_names.txt', 'w', encoding='utf-8') as fw:
    for i, m in enumerate(missing):
        fw.write(f"{i+1}. {m['name']}\n")
