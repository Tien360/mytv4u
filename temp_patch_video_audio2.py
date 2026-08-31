import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject _videoKey
video_key_search = """                                  _buildSectionTitle(
                                    Icons.play_circle_outline,
                                    L10n.t('video_player'),
                                  ),"""
video_key_replace = """                                  SizedBox(key: _videoKey),
                                  _buildSectionTitle(
                                    Icons.play_circle_outline,
                                    L10n.t('video_player'),
                                  ),"""
idx = content.find(video_key_search)
if idx != -1:
    content = content[:idx] + video_key_replace + content[idx+len(video_key_search):]
    print("Injected _videoKey SizedBox")

# 2. Inject Audio Player section after hw_accel
hw_accel_search = """                                              _syncToFirebase();
                                            },
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),"""
                                  
audio_section = """
                                  const SizedBox(height: 48),
                                  SizedBox(key: _audioKey),
                                  _buildSectionTitle(
                                    Icons.music_note,
                                    L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
                                  ),
                                  const SizedBox(height: 16),
                                  GlassContainer(
                                    padding: const EdgeInsets.all(16),
                                    child: Column(
                                      children: [
                                        ListTile(
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
                                        ),
                                      ],
                                    ),
                                  ),"""

idx_end = content.find(hw_accel_search)
if idx_end != -1:
    content = content[:idx_end] + hw_accel_search + audio_section + content[idx_end+len(hw_accel_search):]
    print("Injected Audio section successfully!")
else:
    print("Could not find hw_accel section end")
    # Try another way
    idx_color = content.find("SizedBox(key: _sourcesKey),")
    if idx_color != -1:
        content = content[:idx_color] + audio_section.strip() + "\n                                  const SizedBox(height: 48),\n                                  " + content[idx_color:]
        print("Injected Audio section via fallback!")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
