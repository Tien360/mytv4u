import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Add right-click listener to Scaffold
if "Listener(" not in content:
    content = content.replace("return Scaffold(", '''return Listener(
      onPointerDown: (event) {
        if (event.buttons == 2) { // Right click
          _showAudioSettings();
        }
      },
      child: Scaffold(''').replace("    );\n  }\n}", "    );\n    }\n  }\n}") # Fix closing brace

# 2. Rewrite _showAudioSettings to use Dialog & GlassContainer
old_settings = '''  void _showAudioSettings() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => StatefulBuilder(
        builder: (context, setSheetState) {
          return Container(
            decoration: BoxDecoration(
              color: Colors.grey[900]?.withOpacity(0.95),
              borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
              border: Border(top: BorderSide(color: Colors.white.withOpacity(0.1))),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(height: 12),
                Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(10))),
                const SizedBox(height: 16),
                const Text("Cài đặt Trình phát", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                ListTile(
                  leading: const Icon(Icons.graphic_eq, color: Colors.white70),
                  title: const Text('Hiệu ứng sóng âm', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<String>(
                    dropdownColor: Colors.grey[850],
                    value: visualizerType,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 'bars', child: Text('Cột sóng', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 'waves', child: Text('Lượn sóng', style: TextStyle(color: Colors.white))),
                    ],
                    onChanged: (val) async {
                      if (val != null) {
                        final prefs = await SharedPreferences.getInstance();
                        prefs.setString('audio_visualizer', val);
                        setSheetState(() => visualizerType = val);
                        setState(() => visualizerType = val);
                      }
                    },
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.timer, color: Colors.white70),
                  title: const Text('Hẹn giờ tắt (phút)', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<int>(
                    dropdownColor: Colors.grey[850],
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
                        setSheetState(() => sleepTimerMinutes = val);
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
                  leading: const Icon(Icons.repeat, color: Colors.white70),
                  title: const Text('Chế độ lặp lại', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<int>(
                    dropdownColor: Colors.grey[850],
                    value: repeatMode,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 0, child: Text('Không lặp', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 1, child: Text('Lặp danh sách', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 2, child: Text('Lặp 1 bài', style: TextStyle(color: Colors.white))),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setSheetState(() => repeatMode = val);
                        setState(() => repeatMode = val);
                      }
                    },
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          );
        }
      )
    );
  }'''

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
  }'''

if "void _showAudioSettings() {" in content:
    content = content.replace(old_settings, new_settings)
    if "import 'dart:ui' as ui;" not in content:
        content = "import 'dart:ui' as ui;\n" + content
        
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
