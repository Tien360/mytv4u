import re

content = open('lib/screens/sport_screen.dart', 'r', encoding='utf-8').read()

content = content.replace("? ' Nguồn phát'", "? L10n.t('sources-count')?.replaceAll('{count}', match.sources.length.toString()) ?? ' Nguồn phát'")

open('lib/screens/sport_screen.dart', 'w', encoding='utf-8').write(content)
