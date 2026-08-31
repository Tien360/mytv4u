import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('assets/langs/vi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for k, v in data.items():
    if isinstance(v, str) and ('tối giản' in v.lower() or 'minimal' in k.lower()):
        print(f"{k}: {v}")
