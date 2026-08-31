import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

start_str = '].path!),'
end_str = '                          ],\n                        ),'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + '                          ],\n                        ),' + content[end_idx + len(end_str):]
    open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
