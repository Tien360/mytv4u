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
                                              _syncToFirebase();
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
                                              _syncToFirebase();
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
                                              _syncToFirebase();
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
                                                  _syncToFirebase();
                                                }
                                              },
                                            ),
                                          ),
                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('skip_intro') ?? 'Bỏ qua Intro tự động', style: const TextStyle(color: Colors.white)),
                                            value: _prefs?.getBool('enable_skip_intro') ?? true,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              setState(() {
                                                _prefs?.setBool('enable_skip_intro', val);
                                              });
                                              _syncToFirebase();
                                            },
                                          ),
                                          if (_prefs?.getBool('enable_skip_intro') ?? true) ...[
                                            ListTile(
                                              contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                              title: Text(L10n.t('skip_intro_duration') ?? 'Thời lượng bỏ qua', style: const TextStyle(color: Colors.white)),
                                              trailing: SizedBox(
                                                width: 150,
                                                child: Row(
                                                  children: [
                                                    Expanded(
                                                      child: Slider(
                                                        value: (_prefs?.getInt('skip_intro_duration') ?? 85).toDouble(),
                                                        min: 10,
                                                        max: 180,
                                                        divisions: 34,
                                                        activeColor: Colors.blueAccent,
                                                        onChanged: (val) async {
                                                          setState(() {
                                                            _prefs?.setInt('skip_intro_duration', val.toInt());
                                                          });
                                                          _syncToFirebase();
                                                        },
                                                      ),
                                                    ),
                                                    Text('${_prefs?.getInt('skip_intro_duration') ?? 85}s', style: const TextStyle(color: Colors.amber)),
                                                  ],
                                                ),
                                              ),
                                            ),
                                          ],"""

replace_target = """                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(height: 48),

                                    SizedBox(key: _audioKey),"""

replacement = """                                          ),\n""" + video_ui + """
                                        ],
                                      ),
                                    ),
                                    const SizedBox(height: 48),

                                    SizedBox(key: _audioKey),"""

if 'auto_next_ep' not in content:
    content = content.replace(replace_target, replacement)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched video section correctly!")
