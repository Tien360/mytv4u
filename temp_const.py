import re
with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("const Text(\n                              L10n.t('guest_stars')", "Text(\n                              L10n.t('guest_stars')")
c = c.replace("const Text(L10n.t('guest_stars')", "Text(L10n.t('guest_stars')")
c = c.replace("const Text(\n                                  L10n.t('guest_stars')", "Text(\n                                  L10n.t('guest_stars')")

# Remove any remaining const before Text(L10n
c = re.sub(r"const\s+Text\(\s*L10n\.t", r"Text(L10n.t", c)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed const from Text(L10n...)")
