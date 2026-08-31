import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_viz = '''                                value: ['inline', 'bars', 'circle'].contains(visualizerType) ? visualizerType : 'inline',
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                ],'''

new_viz = '''                                value: ['none', 'inline', 'bars', 'circle'].contains(visualizerType) ? visualizerType : 'bars',
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                ],'''

content = content.replace(old_viz, new_viz)

old_settings_insert = '''                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),'''

new_settings_insert = '''                            ListTile(
                              leading: const Icon(Icons.album, color: Colors.white),
                              title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white)),
                              trailing: Switch(
                                value: showVinyl,
                                activeColor: Colors.blueAccent,
                                onChanged: (val) async {
                                  final prefs = await SharedPreferences.getInstance();
                                  prefs.setBool('audio_vinyl', val);
                                  setDialogState(() => showVinyl = val);
                                  setState(() => showVinyl = val);
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),'''

content = content.replace(old_settings_insert, new_settings_insert)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
