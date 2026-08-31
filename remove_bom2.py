path = 'lib/screens/audio_player_screen.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\uFEFF', '')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
