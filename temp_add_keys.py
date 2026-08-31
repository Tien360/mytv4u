import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

video_audio_code = '''                                  SizedBox(key: _videoKey),
                                  _buildSectionTitle(
                                    Icons.play_circle_outline,
                                    L10n.t('video_player') ?? 'Trình phát Video',
                                  ),
                                  const SizedBox(height: 16),
                                  GlassContainer(
                                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                    child: Column(
                                      children: [
                                        SwitchListTile(
                                          contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                          title: Text(L10n.t('enable_hw_accel') ?? 'Tăng tốc phần cứng (HW Acceleration)', style: const TextStyle(color: Colors.white)),
                                          subtitle: Text(L10n.t('enable_hw_accel_sub') ?? 'Sử dụng GPU để giải mã video, giảm tải CPU và tiết kiệm pin.', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                          value: _prefs?.getBool('enable_hw_accel') ?? true,
                                          activeColor: Colors.blueAccent,
                                          onChanged: (val) {
                                            _prefs?.setBool('enable_hw_accel', val);
                                            setState(() {});
                                            _syncToFirebase();
                                          },
                                        ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(height: 48),

                                  SizedBox(key: _audioKey),
                                  _buildSectionTitle(
                                    Icons.library_music,
                                    L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
                                  ),
                                  const SizedBox(height: 16),
                                  GlassContainer(
                                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                    child: Column(
                                      children: [
                                        ListTile(
                                          contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                          leading: const Icon(Icons.graphic_eq, color: Colors.white),
                                          title: Text(L10n.t('visualizer_type') ?? 'Kiểu sóng âm', style: const TextStyle(color: Colors.white)),
                                          trailing: DropdownButton<String>(
                                            dropdownColor: Colors.grey[900],
                                            value: ['none', 'inline', 'bars', 'circle'].contains(_prefs?.getString('audio_visualizer')) ? _prefs?.getString('audio_visualizer') : 'bars',
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                              DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                            ],
                                            onChanged: (val) {
                                              if (val != null) {
                                                _prefs?.setString('audio_visualizer', val);
                                                setState(() {});
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                        const Divider(color: Colors.white12, height: 32),
                                        ListTile(
                                          contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                          leading: const Icon(Icons.album, color: Colors.white),
                                          title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white)),
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
                                        const Divider(color: Colors.white12, height: 32),
                                        ListTile(
                                          contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                          leading: const Icon(Icons.timer, color: Colors.white),
                                          title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white)),
                                          trailing: DropdownButton<int>(
                                            dropdownColor: Colors.grey[900],
                                            value: [0, 15, 30, 45, 60].contains(_prefs?.getInt('audio_sleep_timer') ?? 0) ? (_prefs?.getInt('audio_sleep_timer') ?? 0) : 0,
                                            underline: const SizedBox(),
                                            items: [0, 15, 30, 45, 60].map((v) => DropdownMenuItem(value: v, child: Text(v == 0 ? (L10n.t('viz_none') ?? 'Tắt') : f'{v}', style: const TextStyle(color: Colors.white)))).toList(),
                                            onChanged: (val) {
                                              if (val != null) {
                                                _prefs?.setInt('audio_sleep_timer', val);
                                                setState(() {});
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(height: 48),

'''

content = content.replace("SizedBox(key: _colorKey)", video_audio_code + "                                  SizedBox(key: _colorKey)")
open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
