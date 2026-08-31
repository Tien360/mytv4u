import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

# Fix the audio block: delete everything between "ListTile( ... vinyl_effect" and "ListTile( ... sleep_timer" 
# and replace it with the correct closing.
start_str = "                                          title: Text(L10n.t('vinyl_effect')"
start_idx = content.find(start_str)
end_str = "                                        const Divider(color: Colors.white12, height: 32);\n                                        ListTile("
# actually just find the next sleep_timer
end_idx = content.find("                                        const Divider(color: Colors.white12, height: 32);\n                                        ListTile(", start_idx)
if end_idx == -1:
    end_idx = content.find("                                        const Divider(color: Colors.white12, height: 32);\r\n                                        ListTile(", start_idx)
if end_idx == -1:
    end_idx = content.find("                                        const Divider(color: Colors.white12, height: 32);\n                                         ListTile(", start_idx) # try something else
if end_idx == -1:
    # Just find `const Divider(color: Colors.white12, height: 32)` followed by sleep_timer
    end_idx = content.find("                                        const Divider(color: Colors.white12, height: 32)", start_idx)

good_audio_part = """                                          title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white)),
                                          trailing: Switch(
                                            value: _prefs?.getBool('audio_vinyl') ?? true,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) {
                                              _prefs?.setBool('audio_vinyl', val);
                                              setState(() {});
                                              _syncToFirebase();
                                            },
                                          ),
                                        ),
"""
content = content[:start_idx] + good_audio_part + content[end_idx:]

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Fixed audio block syntax!")
