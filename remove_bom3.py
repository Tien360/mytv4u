import sys
content = open('lib/screens/audio_player_screen.dart', 'rb').read()
for i, b in enumerate(content):
    if b == 0xEF and content[i+1] == 0xBB and content[i+2] == 0xBF:
        print(f"BOM found at index {i}")
content = content.replace(b'\xef\xbb\xbf', b'')
open('lib/screens/audio_player_screen.dart', 'wb').write(content)
print("Removed BOM bytes.")
