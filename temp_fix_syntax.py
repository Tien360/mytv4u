with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("${L10n.t('season') ?? 'Phần'} ${s['season_number']}", "'${L10n.t('season') ?? 'Phần'} ${s['season_number']}'")
c = c.replace("${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}", "'${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}'")
c = c.replace("'${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}': $name", "'${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}: $name'")
c = c.replace("const Text(L10n.t('director')", "Text(L10n.t('director')")
c = c.replace("const Text(L10n.t('writer')", "Text(L10n.t('writer')")
c = c.replace("const Text(L10n.t('guest_stars')", "Text(L10n.t('guest_stars')")

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed syntax errors!")
