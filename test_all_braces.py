with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()
open_b = text.count("{")
close_b = text.count("}")
print(f"Total open: {open_b}, close: {close_b}, diff: {open_b - close_b}")
