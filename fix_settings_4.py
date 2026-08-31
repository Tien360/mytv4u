content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

ui_code = '''
                                  const SizedBox(height: 48),
                                  
                                  SizedBox(key: _audioKey),
                                  _buildSectionTitle(
                                    Icons.library_music,
                                    L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
                                  ),
                                  const SizedBox(height: 16),
                                  GlassContainer(
                                    padding: const EdgeInsets.all(16),
                                    child: Column(
                                      children: [
                                        ListTile(
                                          leading: const Icon(Icons.graphic_eq, color: Colors.white),
                                          title: Text(L10n.t('visualizer_type') ?? 'Kiểu sóng âm', style: const TextStyle(color: Colors.white)),
                                          trailing: DropdownButton<String>(
                                            dropdownColor: Colors.grey[900],
                                            value: ['none', 'inline', 'bars', 'circle'].contains(_visualizerType) ? _visualizerType : 'bars',
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                final prefs = await SharedPreferences.getInstance();
                                                prefs.setString('audio_visualizer', val);
                                                setState(() => _visualizerType = val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        ListTile(
                                          leading: const Icon(Icons.album, color: Colors.white),
                                          title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white)),
                                          trailing: Switch(
                                            value: _showVinyl,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              final prefs = await SharedPreferences.getInstance();
                                              prefs.setBool('audio_vinyl', val);
                                              setState(() => _showVinyl = val);
                                              _syncToFirebase();
                                            },
                                          ),
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        ListTile(
                                          leading: const Icon(Icons.timer, color: Colors.white),
                                          title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white)),
                                          trailing: DropdownButton<int>(
                                            dropdownColor: Colors.grey[900],
                                            value: _sleepTimerMinutes,
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 0, child: Text(L10n.t('off') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 15, child: const Text('15', style: TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 30, child: const Text('30', style: TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 60, child: const Text('60', style: TextStyle(color: Colors.white))),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                final prefs = await SharedPreferences.getInstance();
                                                prefs.setInt('audio_sleep_timer', val);
                                                setState(() => _sleepTimerMinutes = val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
'''
content = content.replace('SizedBox(key: _colorKey)', ui_code + '\n                                  SizedBox(key: _colorKey)')

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
