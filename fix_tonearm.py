content = open('lib/widgets/tonearm_widget.dart', 'r', encoding='utf-8').read()
content = content.replace('Colors.redAccent', 'Paint()..color=Colors.redAccent')
open('lib/widgets/tonearm_widget.dart', 'w', encoding='utf-8').write(content)
