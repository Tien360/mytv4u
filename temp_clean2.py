import re
with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = re.sub(r"L10n\.t\('director'\) \?\? '[^']*'", "L10n.t('director')", c)
c = re.sub(r"L10n\.t\('writer'\) \?\? '[^']*'", "L10n.t('writer')", c)
c = re.sub(r"L10n\.t\('guest_stars'\) \?\? '[^']*'", "L10n.t('guest_stars')", c)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Cleaned up missing strings!")
