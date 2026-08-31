import os

# 1. Fix library_screen.dart
content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('FilePicker.platform.pickFiles', 'FilePicker.pickFiles')
content = content.replace("replace('\\\\\\\\', '/')", "replaceAll('\\\\\\\\', '/')")
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)

# 2. Fix audio_player_screen.dart strings
content_audio = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
content_audio = content_audio.replace('const Text("Audio Player")', 'Text(L10n.t(\\'audio_player_title\\') ?? "Audio Player")')
if "import '../utils/l10n.dart';" not in content_audio:
    content_audio = "import '../utils/l10n.dart';\n" + content_audio
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content_audio)

# 3. Add to vi.json and en.json
import json
def update_json(file, key, val):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[key] = val
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json('assets/langs/vi.json', 'audio_player_title', 'Trình phát Nhạc')
update_json('assets/langs/en.json', 'audio_player_title', 'Audio Player')
