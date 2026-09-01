import re
with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = re.sub(r"L10n\.t\('error_tmdb_id_not_found'\) \?\? '[^']*'", "L10n.t('error_tmdb_id_not_found')", c)
c = re.sub(r"L10n\.t\('error_no_seasons'\) \?\? '[^']*'", "L10n.t('error_no_seasons')", c)
c = re.sub(r"L10n\.t\('error_no_valid_seasons'\) \?\? '[^']*'", "L10n.t('error_no_valid_seasons')", c)

c = re.sub(r"L10n\.t\('error_prefix'\) != null \? '\$\{L10n\.t\('error_prefix'\)\}: \$e' : '[^']*'", "'${L10n.t('error_prefix')}: $e'", c)
c = re.sub(r"L10n\.t\('error_loading_episodes'\) != null \? '\$\{L10n\.t\('error_loading_episodes'\)\}: \$e' : '[^']*'", "'${L10n.t('error_loading_episodes')}: $e'", c)

c = re.sub(r"L10n\.t\('season'\) \?\? '[^']*'", "L10n.t('season')", c)
c = re.sub(r"L10n\.t\('episode'\) \?\? '[^']*'", "L10n.t('episode')", c)
c = re.sub(r"L10n\.t\('released'\) \?\? '[^']*'", "L10n.t('released')", c)
c = re.sub(r"L10n\.t\('upcoming'\) \?\? '[^']*'", "L10n.t('upcoming')", c)
c = re.sub(r"L10n\.t\('minutes'\) \?\? '[^']*'", "L10n.t('minutes')", c)
c = re.sub(r"L10n\.t\('votes'\) \?\? '[^']*'", "L10n.t('votes')", c)
c = re.sub(r"L10n\.t\('air_schedule'\) \?\? '[^']*'", "L10n.t('air_schedule')", c)
c = re.sub(r"L10n\.t\('no_schedule_found'\) \?\? '[^']*'", "L10n.t('no_schedule_found')", c)
c = re.sub(r"L10n\.t\('air_date'\) \?\? '[^']*'", "L10n.t('air_date')", c)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Cleaned up dart file!")
