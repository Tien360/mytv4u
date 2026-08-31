import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("void _showAudioSettings()")
if idx != -1:
    print(content[idx+4500:idx+6000])
