import re

content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()
content = content.replace("const Text(\n                          L10n.t('open-link')", "Text(\n                          L10n.t('open-link')")
content = content.replace("const Text(\n                          L10n.t('open-file')", "Text(\n                          L10n.t('open-file')")
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)
