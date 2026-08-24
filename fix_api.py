import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_logic = """        merged = merged.copyWith(
            thumbUrl: merged.thumbUrl.isNotEmpty
                ? merged.thumbUrl
                : item.thumbUrl,"""

new_logic = """        merged = merged.copyWith(
            name: merged.name.isNotEmpty ? merged.name : item.name,
            originalName: merged.originalName.isNotEmpty ? merged.originalName : item.originalName,
            thumbUrl: merged.thumbUrl.isNotEmpty
                ? merged.thumbUrl
                : item.thumbUrl,"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed copyWith in phim_api.dart!")
else:
    print("Old logic not found!")
