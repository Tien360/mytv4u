import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_logic = """        merged = merged.copyWith(
            name: merged.name.isNotEmpty ? merged.name : item.name,
            originalName: merged.originalName.isNotEmpty ? merged.originalName : item.originalName,
            thumbUrl: merged.thumbUrl.isNotEmpty"""

text = re.sub(r'merged = merged\.copyWith\(\s*thumbUrl: merged\.thumbUrl\.isNotEmpty', new_logic, text)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Regex replaced copyWith in phim_api.dart!")
