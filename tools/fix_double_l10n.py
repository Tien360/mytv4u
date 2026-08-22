import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix L10n.t('xxx') ?? \n L10n.t('xxx') ??
content = re.sub(r"L10n\.t\('([^']+)'\)\s*\?\?\s*L10n\.t\('\1'\)\s*\?\?", r"L10n.t('\1') ??", content)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed double L10n.t')
