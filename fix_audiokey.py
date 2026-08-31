import os
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('final GlobalKey _subtitleKey = GlobalKey();', 'final GlobalKey _subtitleKey = GlobalKey();\n  final GlobalKey _audioKey = GlobalKey();')
open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
