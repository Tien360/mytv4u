import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_settings = '''                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),'''
                              
new_settings = '''                            ListTile(
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
                              leading: const Icon(Icons.timer, color: Colors.white),'''
                              
content = content.replace(old_settings, new_settings)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
