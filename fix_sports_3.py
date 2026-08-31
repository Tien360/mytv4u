import re

content = open('lib/screens/sport_screen.dart', 'r', encoding='utf-8').read()

content = content.replace("L10n.t(live-ongoing)", "L10n.t('live-ongoing')")
content = content.replace("L10n.t(live-upcoming)", "L10n.t('live-upcoming')")
content = content.replace("L10n.t(live-schedule-scores)", "L10n.t('live-schedule-scores')")

open('lib/screens/sport_screen.dart', 'w', encoding='utf-8').write(content)
