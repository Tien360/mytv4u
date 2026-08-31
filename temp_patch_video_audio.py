import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract the Video Settings chunk
# It starts at the Divider before `auto_next`
# `auto_next` starts with `SwitchListTile(`
start_search = """                                        const Divider(
                                          color: Colors.white12,
                                          height: 1,
                                        ),
                                        SwitchListTile(
                                          title: Text(
                                            L10n.t('auto_next'),"""
                                            
idx_start = content.find(start_search)
if idx_start == -1:
    print("Could not find start of video settings")
    sys.exit(1)

# It ends after `hw_accel`
end_search = """                                              _syncToFirebase();
                                            },
                                          ),"""
idx_end = content.find(end_search, content.find("L10n.t('hw_accel')"))
if idx_end == -1:
    print("Could not find end of video settings")
    sys.exit(1)

idx_end += len(end_search)

video_chunk = content[idx_start:idx_end]

# 2. Delete the Video Settings chunk from its original place
content = content[:idx_start] + content[idx_end:]

# 3. Create the new Video and Audio blocks
video_section = """
                                  const SizedBox(height: 48),
                                  SizedBox(key: _videoKey),
                                  _buildSectionTitle(
                                    Icons.play_circle_filled,
                                    L10n.t('player_settings') ?? 'Trình phát Phim',
                                  ),
                                  const SizedBox(height: 16),
                                  GlassContainer(
                                    padding: const EdgeInsets.all(16),
                                    child: Column(
                                      children: [
""" + video_chunk.replace("                                        ", "                                        ") + """
                                      ],
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

# 4. Inject them before `_colorKey`
inject_search = "                                  SizedBox(key: _colorKey),"
idx_inject = content.find(inject_search)
if idx_inject != -1:
    content = content[:idx_inject] + video_section + audio_section + "\n" + content[idx_inject:]
    print("Injected video and audio sections successfully!")
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find _colorKey injection point")
