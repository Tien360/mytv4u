import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

audio_section_old = """                                        ListTile(
                                          title: Text(L10n.t('audio_visualizer') ?? 'Hiệu ứng âm thanh', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          trailing: DropdownButton<String>(
                                            value: _audioVisualizer,
                                            dropdownColor: Colors.black87,
                                            style: const TextStyle(color: Colors.amber, fontSize: 16),
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt')),
                                              DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)')),
                                              DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)')),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                setState(() => _audioVisualizer = val);
                                                final p = await SharedPreferences.getInstance();
                                                await p.setString('audio_visualizer', val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        SwitchListTile(
                                          title: Text(L10n.t('audio_vinyl') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          subtitle: Text(L10n.t('audio_vinyl_desc') ?? 'Xoay ảnh bìa bài hát', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                          value: _audioVinyl,
                                          activeColor: Colors.amber,
                                          onChanged: (val) async {
                                            setState(() => _audioVinyl = val);
                                            final p = await SharedPreferences.getInstance();
                                            await p.setBool('audio_vinyl', val);
                                            _syncToFirebase();
                                          },
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        ListTile(
                                          title: Text(L10n.t('audio_sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          trailing: DropdownButton<int>(
                                            value: _audioSleepTimer,
                                            dropdownColor: Colors.black87,
                                            style: const TextStyle(color: Colors.amber, fontSize: 16),
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 0, child: Text(L10n.t('timer_off') ?? 'Tắt')),
                                              DropdownMenuItem(value: 15, child: const Text('15')),
                                              DropdownMenuItem(value: 30, child: const Text('30')),
                                              DropdownMenuItem(value: 60, child: const Text('60')),
                                              DropdownMenuItem(value: 120, child: const Text('120')),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                setState(() => _audioSleepTimer = val);
                                                final p = await SharedPreferences.getInstance();
                                                await p.setInt('audio_sleep_timer', val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),"""
                                        
audio_section_new = """                                        ListTile(
                                          title: Text(L10n.t('visualizer_type') ?? 'Kiểu sóng âm', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          trailing: DropdownButton<String>(
                                            value: ['none', 'inline', 'bars', 'circle'].contains(_audioVisualizer) ? _audioVisualizer : 'bars',
                                            dropdownColor: Colors.black87,
                                            style: const TextStyle(color: Colors.amber, fontSize: 16),
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt')),
                                              DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)')),
                                              DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)')),
                                              DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa')),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                setState(() => _audioVisualizer = val);
                                                final p = await SharedPreferences.getInstance();
                                                await p.setString('audio_visualizer', val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        SwitchListTile(
                                          title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          subtitle: Text(L10n.t('audio_vinyl_desc') ?? 'Mô phỏng đĩa than xoay khi phát nhạc', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                          value: _audioVinyl,
                                          activeColor: Colors.amber,
                                          onChanged: (val) async {
                                            setState(() => _audioVinyl = val);
                                            final p = await SharedPreferences.getInstance();
                                            await p.setBool('audio_vinyl', val);
                                            _syncToFirebase();
                                          },
                                        ),
                                        const Divider(color: Colors.white12, height: 1),
                                        ListTile(
                                          title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                          trailing: DropdownButton<int>(
                                            value: _audioSleepTimer,
                                            dropdownColor: Colors.black87,
                                            style: const TextStyle(color: Colors.amber, fontSize: 16),
                                            underline: const SizedBox(),
                                            items: [
                                              DropdownMenuItem(value: 0, child: Text(L10n.t('off') ?? 'Tắt')),
                                              DropdownMenuItem(value: 15, child: const Text('15')),
                                              DropdownMenuItem(value: 30, child: const Text('30')),
                                              DropdownMenuItem(value: 60, child: const Text('60')),
                                            ],
                                            onChanged: (val) async {
                                              if (val != null) {
                                                setState(() => _audioSleepTimer = val);
                                                final p = await SharedPreferences.getInstance();
                                                await p.setInt('audio_sleep_timer', val);
                                                _syncToFirebase();
                                              }
                                            },
                                          ),
                                        ),"""
                                        
idx = content.find(audio_section_old)
if idx != -1:
    content = content.replace(audio_section_old, audio_section_new)
    print("Replaced audio section in settings_screen.dart!")
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find old audio section!")
