import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

video_block = """                                            const Divider(color: Colors.white12, height: 1),
                                            SwitchListTile(
                                              contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                              title: Text(L10n.t('skip_intro') ?? 'Bỏ qua Intro tự động', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                              value: _prefs?.getBool('enable_skip_intro') ?? false,
                                              activeColor: Colors.amber,
                                              onChanged: (val) async {
                                                final prefs = await SharedPreferences.getInstance();
                                                await prefs.setBool('enable_skip_intro', val);
                                                setState(() {});
                                                _syncToFirebase();
                                              },
                                            ),
                                            if (_prefs?.getBool('enable_skip_intro') ?? false) ...[
                                              ListTile(
                                                contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                                title: Text(L10n.t('skip_intro_duration') ?? 'Thời lượng bỏ qua', style: const TextStyle(color: Colors.white70)),
                                                trailing: SizedBox(
                                                  width: 150,
                                                  child: Row(
                                                    mainAxisAlignment: MainAxisAlignment.end,
                                                    children: [
                                                      Text('${_prefs?.getInt('skip_intro_duration') ?? 85} s', style: const TextStyle(color: Colors.white70)),
                                                      const SizedBox(width: 8),
                                                      Expanded(
                                                        child: Slider(
                                                          value: (_prefs?.getInt('skip_intro_duration') ?? 85).toDouble(),
                                                          min: 30,
                                                          max: 180,
                                                          divisions: 30,
                                                          onChanged: (val) async {
                                                            final prefs = await SharedPreferences.getInstance();
                                                            await prefs.setInt('skip_intro_duration', val.toInt());
                                                            setState(() {});
                                                            _syncToFirebase();
                                                          },
                                                        ),
                                                      ),
                                                    ],
                                                  ),
                                                ),
                                              ),
                                            ],
                                            const Divider(color: Colors.white12, height: 1),
                                            SwitchListTile(
                                              contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                              title: Text(L10n.t('background_playback') ?? 'Phát dưới nền', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                              subtitle: Text(L10n.t('background_playback_sub') ?? 'Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                              value: _prefs?.getBool('background_playback') ?? false,
                                              activeColor: Colors.amber,
                                              onChanged: (val) async {
                                                final prefs = await SharedPreferences.getInstance();
                                                await prefs.setBool('background_playback', val);
                                                setState(() {});
                                                _syncToFirebase();
                                              },
                                            ),
"""

# We inject this AFTER 'default_speed' block
search_str = """                                                    'default_speed',
                                                    val,
                                                  );
                                                  _syncToFirebase();
                                                }
                                              },
                                            ),
                                          ),"""

idx = content.find(search_str)
if idx != -1:
    end_idx = idx + len(search_str)
    content = content[:end_idx] + "\n" + video_block + content[end_idx:]
    print("Injected video block via absolute string match!")
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find default_speed block!")
