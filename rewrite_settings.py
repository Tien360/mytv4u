import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

start_idx = content.find('  void _showAudioSettings() {')
end_idx = content.find('  Future<Uint8List?> _getCoverForFile')

new_settings = '''  void _showAudioSettings() {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: Container(
              width: 500,
              decoration: BoxDecoration(
                color: const Color(0x33000000),
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: const Color(0x33FFFFFF)),
                boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 20)],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: BackdropFilter(
                  filter: ui.ImageFilter.blur(sigmaX: 40, sigmaY: 40),
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: StatefulBuilder(
                      builder: (context, setDialogState) {
                        return Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(L10n.t('audio_settings') ?? "Cài đặt Trình phát", style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 24),
                            ListTile(
                              leading: const Icon(Icons.graphic_eq, color: Colors.white),
                              title: Text(L10n.t('visualizer_type') ?? 'Kiểu sóng âm', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<String>(
                                dropdownColor: Colors.grey[900],
                                value: ['inline', 'bars', 'circle'].contains(visualizerType) ? visualizerType : 'inline',
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) async {
                                  if (val != null) {
                                    final prefs = await SharedPreferences.getInstance();
                                    prefs.setString('audio_visualizer', val);
                                    setDialogState(() => visualizerType = val);
                                    setState(() => visualizerType = val);
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),
                              title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: sleepTimerMinutes,
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
                                    setDialogState(() => sleepTimerMinutes = val);
                                    setState(() => sleepTimerMinutes = val);
                                    if (val > 0) {
                                      Future.delayed(Duration(minutes: val), () {
                                        if (mounted) player.pause();
                                      });
                                    }
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.repeat, color: Colors.white),
                              title: Text(L10n.t('repeat_mode') ?? 'Chế độ lặp lại', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: repeatMode,
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 0, child: Text(L10n.t('repeat_none') ?? 'Không lặp', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 1, child: Text(L10n.t('repeat_all') ?? 'Lặp danh sách', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 2, child: Text(L10n.t('repeat_one') ?? 'Lặp 1 bài', style: const TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) {
                                  if (val != null) {
                                    setDialogState(() => repeatMode = val);
                                    setState(() => repeatMode = val);
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.keyboard, color: Colors.white),
                              title: Text(L10n.t('shortcuts') ?? 'Phím tắt', style: const TextStyle(color: Colors.white)),
                              trailing: const Text('Space, ←/→, M, S, R', style: TextStyle(color: Colors.white54, fontSize: 14)),
                            ),
                            ListTile(
                              leading: const Icon(Icons.info_outline, color: Colors.white),
                              title: Text(L10n.t('audio_quality') ?? 'Chất lượng âm thanh', style: const TextStyle(color: Colors.white)),
                              trailing: Builder(
                                builder: (context) {
                                  String qualityInfo = L10n.t('unknown') ?? "Chưa rõ";
                                  if (duration.inSeconds > 0 && _playlistFiles.isNotEmpty) {
                                    try {
                                      int bytes = File(_playlistFiles[currentIndex].path!).lengthSync();
                                      int kbps = ((bytes * 8) / duration.inSeconds / 1000).round();
                                      qualityInfo = " kbps";
                                      if (kbps > 320) qualityInfo += " (Lossless)";
                                      else if (kbps >= 256) qualityInfo += " (HQ)";
                                      else if (kbps >= 128) qualityInfo += " (Standard)";
                                    } catch (e) {
                                      qualityInfo = L10n.t('error_read_file') ?? "Lỗi đọc file";
                                    }
                                  }
                                  return Text(qualityInfo, style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold));
                                }
                              ),
                            ),
                          ],
                        );
                      }
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      }
    );
  }

'''

content = content[:start_idx] + new_settings + content[end_idx:]
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
