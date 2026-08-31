import sys, re
with open("lib/utils/l10n.dart", "r", encoding="utf-8") as f:
    c = f.read()

def insert_dict(c, dict_name, keys_str):
    pattern = rf"(static const Map<String, String> {dict_name} = {{)"
    replacement = rf"\1\n{keys_str}"
    return re.sub(pattern, replacement, c)

en_keys = """    'air_schedule': 'Air Schedule',
    'no_schedule_found': 'No TMDB schedule info found.',
    'air_date': 'Air Date',"""

vi_keys = """    'air_schedule': 'Lịch phát sóng',
    'no_schedule_found': 'Chưa có thông tin lịch chiếu từ TMDB.',
    'air_date': 'Ngày chiếu',"""

c = insert_dict(c, "_en", en_keys)
c = insert_dict(c, "_vi", vi_keys)

with open("lib/utils/l10n.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated l10n")
