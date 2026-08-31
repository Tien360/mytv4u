import os
content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('Text("Bỏ qua Intro"', "Text(L10n.t('skip_intro') ?? 'Bỏ qua Intro'")
open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
