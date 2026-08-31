import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

# Replace divider heights in Audio Player block
audio_start = content.find("SizedBox(key: _audioKey)")
audio_end = content.find("SizedBox(key: _colorKey)")
audio_code = content[audio_start:audio_end]

audio_code = audio_code.replace("const Divider(color: Colors.white12, height: 1)", "const Divider(color: Colors.white12, height: 16)")

content = content[:audio_start] + audio_code + content[audio_end:]

# Let's also check Video Player block.
vp_start = content.find("SizedBox(key: _videoKey)")
vp_end = content.find("SizedBox(key: _audioKey)")
vp_code = content[vp_start:vp_end]
vp_code = vp_code.replace("const Divider(color: Colors.white12, height: 1)", "const Divider(color: Colors.white12, height: 16)")
vp_code = vp_code.replace("const Divider(\n                                            color: Colors.white12,\n                                            height: 1,\n                                          )", "const Divider(\n                                            color: Colors.white12,\n                                            height: 16,\n                                          )")

content = content[:vp_start] + vp_code + content[vp_end:]

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
