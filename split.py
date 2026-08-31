content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
idx = content.find('  @override\n  Widget build(BuildContext context) {')
if idx != -1:
    content = content[:idx]
    open('lib/screens/audio_player_screen.dart_part1', 'w', encoding='utf-8').write(content)
