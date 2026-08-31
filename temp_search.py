import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    d = json.load(f)
for k, v in d.items():
    if "webview" in k.lower() or "webview" in str(v).lower():
        print(f"{k}: {v}")
