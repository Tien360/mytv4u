import re

content = open('lib/screens/sport_screen.dart', 'r', encoding='utf-8').read()

# Remove 'const' before tabs list
content = content.replace('tabs: const [', 'tabs: [')
content = content.replace("Tab(text: L10n.t(''live-ongoing'') ?? \"Đang diễn ra (Live)\")", "Tab(text: L10n.t('live-ongoing') ?? \"Đang diễn ra (Live)\")")
content = content.replace("Tab(text: L10n.t(''live-upcoming'') ?? \"Sắp diễn ra\")", "Tab(text: L10n.t('live-upcoming') ?? \"Sắp diễn ra\")")
content = content.replace("Tab(text: L10n.t(''live-schedule-scores'') ?? \"Lịch Thi Đấu & Tỷ Số\")", "Tab(text: L10n.t('live-schedule-scores') ?? \"Lịch Thi Đấu & Tỷ Số\")")

# Fix double quotes inside L10n.t
content = content.replace("L10n.t(''no-live-matches'')", "L10n.t('no-live-matches')")
content = content.replace("L10n.t(''no-upcoming-matches'')", "L10n.t('no-upcoming-matches')")
content = content.replace("L10n.t(''other-leagues'')", "L10n.t('other-leagues')")
content = content.replace("L10n.t(''sources-count'')?.replaceAll(''{count}''", "L10n.t('sources-count')?.replaceAll('{count}'")
content = content.replace("L10n.t(''no-sources-yet'')", "L10n.t('no-sources-yet')")
content = content.replace("L10n.t(''no-schedule-data'')", "L10n.t('no-schedule-data')")

content = content.replace("const Text(L10n.t('no-schedule-data')", "Text(L10n.t('no-schedule-data')")

open('lib/screens/sport_screen.dart', 'w', encoding='utf-8').write(content)
