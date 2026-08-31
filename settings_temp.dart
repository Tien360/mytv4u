  void _showAudioSettings() {
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
                            const Text("Cài đặt Trình phát", style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 24),
                            ListTile(
                              leading: const Icon(Icons.graphic_eq, color: Colors.white),
                              title: const Text('Vị trí & Kiểu sóng âm', style: TextStyle(color: Colors.white)),
                              trailing: DropdownButton<String>(
                                dropdownColor: Colors.grey[900],
                                value: ['inline', 'bars', 'circle'].contains(visualizerType) ? visualizerType : 'inline',
                                underline: const SizedBox(),
                                items: const [
                                  DropdownMenuItem(value: 'inline', child: Text('Nhỏ (cạnh tên)', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'bars', child: Text('Lớn (dưới ảnh)', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'circle', child: Text('Vòng tròn đĩa', style: TextStyle(color: Colors.white))),
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
                              leading: const Icon(Icons.info_outline, color: Colors.white),
                              title: const Text('Chất lượng âm thanh', style: TextStyle(color: Colors.white)),
                              trailing: Builder(
                                builder: (context) {
                                  String qualityInfo = "Chưa rõ";
                                  if (duration.inSeconds > 0) {
                                    try {
                                      int bytes = File(_playlistFiles[currentIndex].path!).lengthSync();
                                      int kbps = ((bytes * 8) / duration.inSeconds / 1000).round();
                                      qualityInfo = " kbps";
                                      if (kbps > 320) qualityInfo += " (Lossless)";
                                      else if (kbps >= 256) qualityInfo += " (HQ)";
                                      else if (kbps >= 128) qualityInfo += " (Standard)";
                                    } catch (e) {
                                      qualityInfo = "Lỗi đọc file";
                                    }
                                  }
                                  return Text(qualityInfo, style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold));
                                }
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),
                              title: const Text('Hẹn giờ tắt (phút)', style: TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: sleepTimerMinutes,
                                underline: const SizedBox(),
                                items: const [
                                  DropdownMenuItem(value: 0, child: Text('Tắt', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 15, child: Text('15', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 30, child: Text('30', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 60, child: Text('60', style: TextStyle(color: Colors.white))),
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
                              title: const Text('Chế độ lặp lại', style: TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: repeatMode,
                                underline: const SizedBox(),
                                items: const [
                                  DropdownMenuItem(value: 0, child: Text('Không lặp', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 1, child: Text('Lặp danh sách', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 2, child: Text('Lặp 1 bài', style: TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) {
                                  if (val != null) {
                                    setDialogState(() => repeatMode = val);
                                    setState(() => repeatMode = val);
                                  }
                                },
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

