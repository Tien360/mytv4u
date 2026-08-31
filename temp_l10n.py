import sys

with open("lib/utils/l10n.dart", "r", encoding="utf-8") as f:
    c = f.read()

en_target = "'episodes': 'Episodes',"
en_new = "'episodes': 'Episodes',\n      'air_schedule': 'Air Schedule',\n      'no_schedule_found': 'No TMDB schedule info found.',\n      'air_date': 'Air Date',"

vi_target = "'episodes': 'Tập',"
vi_new = "'episodes': 'Tập',\n      'air_schedule': 'Lịch phát sóng',\n      'no_schedule_found': 'Chưa có thông tin lịch chiếu từ TMDB.',\n      'air_date': 'Ngày chiếu',"

if en_target in c:
    c = c.replace(en_target, en_new)
if vi_target in c:
    c = c.replace(vi_target, vi_new)

with open("lib/utils/l10n.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated l10n.dart")
