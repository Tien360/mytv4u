import json
with open("assets/langs/vi.json", "rb") as f:
    b = f.read()
print(b[-100:])
