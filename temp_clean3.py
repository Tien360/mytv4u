import re
with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("Text(\"Đang dịch...\",", "Text(L10n.t('translating'),")
c = re.sub(r"L10n\.t\('translated_by_google'\) \?\? '[^']*'", "L10n.t('translated_by_google')", c)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Cleaned up dart file!")
