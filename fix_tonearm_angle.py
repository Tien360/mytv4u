import re

content = open('lib/widgets/tonearm_widget.dart', 'r', encoding='utf-8').read()
content = content.replace('begin: 0.0,', 'begin: -15.0,')
content = content.replace('end: isPlaying ? 25.0 : 0.0', 'end: isPlaying ? 15.0 : -15.0')
open('lib/widgets/tonearm_widget.dart', 'w', encoding='utf-8').write(content)

