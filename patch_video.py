import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

video_ui = """                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('auto_next_ep') ?? 'Tự động chuyển tập', style: const TextStyle(color: Colors.white)),
                                            value: _autoNext,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              setState(() => _autoNext = val);
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('auto_next', val);
                                            },
                                          ),
                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('auto_play_trailer') ?? 'Tự động phát Trailer', style: const TextStyle(color: Colors.white)),
                                            value: _autoPlayTrailer,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              setState(() => _autoPlayTrailer = val);
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('auto_play_trailer', val);
                                            },
                                          ),
                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('bg_playback') ?? 'Phát trong nền', style: const TextStyle(color: Colors.white)),
                                            subtitle: Text('Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 12)),
                                            value: _backgroundPlayback,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              setState(() => _backgroundPlayback = val);
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('background_playback', val);
                                            },
                                          ),
                                          const Divider(color: Colors.white12),
                                          ListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('default_speed') ?? 'Tốc độ phát mặc định', style: const TextStyle(color: Colors.white)),
                                            trailing: DropdownButton<double>(
                                              dropdownColor: Colors.black87,
                                              value: _defaultSpeed,
                                              style: const TextStyle(color: Colors.amber, fontSize: 16),
                                              underline: const SizedBox(),
                                              items: const [
                                                DropdownMenuItem(value: 0.5, child: Text('0.5x')),
                                                DropdownMenuItem(value: 0.75, child: Text('0.75x')),
                                                DropdownMenuItem(value: 1.0, child: Text('1.0x')),
                                                DropdownMenuItem(value: 1.25, child: Text('1.25x')),
                                                DropdownMenuItem(value: 1.5, child: Text('1.5x')),
                                                DropdownMenuItem(value: 2.0, child: Text('2.0x')),
                                              ],
                                              onChanged: (val) async {
                                                if (val != null) {
                                                  setState(() => _defaultSpeed = val);
                                                  final prefs = await SharedPreferences.getInstance();
                                                  await prefs.setDouble('default_speed', val);
                                                }
                                              },
                                            ),
                                          ),"""

if 'auto_next_ep' not in content:
    content = content.replace("                                              _syncToFirebase();\n                                            },\n                                          ),", "                                              _syncToFirebase();\n                                            },\n                                          ),\n" + video_ui)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched video settings!")
