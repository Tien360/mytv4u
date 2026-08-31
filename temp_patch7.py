import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. OPTIMIZER BLOCK
opt_block = """                                          Container(
                                            width: double.infinity,
                                            margin: const EdgeInsets.only(bottom: 16),
                                            decoration: BoxDecoration(
                                              color: Colors.blueAccent.withOpacity(0.1),
                                              borderRadius: BorderRadius.circular(12),
                                              border: Border.all(color: Colors.blueAccent.withOpacity(0.3)),
                                            ),
                                            child: ListTile(
                                              contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                                              leading: const Icon(Icons.speed, color: Colors.blueAccent, size: 32),
                                              title: Text(L10n.t('setting_opt_title') ?? 'Trợ lý Tối ưu hóa (Khuyên dùng)', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                                              subtitle: Text(L10n.t('setting_opt_desc') ?? 'Tự động quét cấu hình máy tính và thiết lập giao diện mượt mà nhất.', style: const TextStyle(color: Colors.white70)),
                                              trailing: ElevatedButton(
                                                style: ElevatedButton.styleFrom(
                                                  backgroundColor: Colors.blueAccent,
                                                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                                ),
                                                onPressed: () async {
                                                  final result = await showDialog(context: context, builder: (_) => const OptimizerDialog());
                                                  if (result != null) {
                                                    _loadSettings();
                                                  }
                                                },
                                                child: Text(L10n.t('setting_opt_btn') ?? 'Quét ngay', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                              ),
                                            ),
                                          ),
"""

if "Trợ lý Tối ưu hóa" not in content and "OptimizerDialog" not in content:
    match_opt = re.search(r'(                                          ListTile\(\s*title: Text\(\s*L10n.t\(\'watch_limit\'\),)', content)
    if match_opt:
        content = content.replace(match_opt.group(1), opt_block + match_opt.group(1))
        if "import '../widgets/optimizer_dialog.dart';" not in content:
            content = content.replace("import '../widgets/custom_title_bar.dart';", "import '../widgets/custom_title_bar.dart';\nimport '../widgets/optimizer_dialog.dart';")
        print("Injected Optimizer block.")

# 2. VIDEO PLAYER BLOCK
video_block = """
                                          const Divider(color: Colors.white12, height: 32),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('auto_next') ?? 'Tự động chuyển tập', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            value: _autoNext,
                                            activeColor: Colors.amber,
                                            onChanged: (val) async {
                                              setState(() => _autoNext = val);
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('auto_next', val);
                                              _syncToFirebase();
                                            },
                                          ),
                                          const Divider(color: Colors.white12, height: 1),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('skip_intro') ?? 'Bỏ qua Intro tự động', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            value: _prefs?.getBool('enable_skip_intro') ?? false,
                                            activeColor: Colors.amber,
                                            onChanged: (val) async {
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('enable_skip_intro', val);
                                              setState(() {});
                                              _syncToFirebase();
                                            },
                                          ),
                                          if (_prefs?.getBool('enable_skip_intro') ?? false) ...[
                                            ListTile(
                                              contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                              title: Text(L10n.t('skip_intro_duration') ?? 'Thời lượng bỏ qua', style: const TextStyle(color: Colors.white70)),
                                              trailing: SizedBox(
                                                width: 150,
                                                child: Row(
                                                  mainAxisAlignment: MainAxisAlignment.end,
                                                  children: [
                                                    Text('${_prefs?.getInt('skip_intro_duration') ?? 85} s', style: const TextStyle(color: Colors.white70)),
                                                    const SizedBox(width: 8),
                                                    Expanded(
                                                      child: Slider(
                                                        value: (_prefs?.getInt('skip_intro_duration') ?? 85).toDouble(),
                                                        min: 30,
                                                        max: 180,
                                                        divisions: 30,
                                                        onChanged: (val) async {
                                                          final prefs = await SharedPreferences.getInstance();
                                                          await prefs.setInt('skip_intro_duration', val.toInt());
                                                          setState(() {});
                                                          _syncToFirebase();
                                                        },
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ),
                                          ],
                                          const Divider(color: Colors.white12, height: 1),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('background_playback') ?? 'Phát dưới nền', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            subtitle: Text('Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                            value: _backgroundPlayback,
                                            activeColor: Colors.amber,
                                            onChanged: (val) async {
                                              setState(() => _backgroundPlayback = val);
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('background_playback', val);
                                              _syncToFirebase();
                                            },
                                          ),
                                          const Divider(color: Colors.white12, height: 1),
                                          ListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text('Tốc độ mặc định (Default Speed)', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            trailing: DropdownButton<double>(
                                              value: _prefs?.getDouble('default_speed') ?? 1.0,
                                              dropdownColor: Colors.black87,
                                              style: const TextStyle(color: Colors.amber, fontSize: 16),
                                              underline: const SizedBox(),
                                              items: [0.5, 0.75, 1.0, 1.25, 1.5, 2.0].map((double value) {
                                                return DropdownMenuItem<double>(
                                                  value: value,
                                                  child: Text('${value}x'),
                                                );
                                              }).toList(),
                                              onChanged: (double? newValue) async {
                                                if (newValue != null) {
                                                  final prefs = await SharedPreferences.getInstance();
                                                  await prefs.setDouble('default_speed', newValue);
                                                  setState(() {});
                                                  _syncToFirebase();
                                                }
                                              },
                                            ),
                                          ),
"""

if "Tốc độ mặc định (Default Speed)" not in content:
    match_video = re.search(r'(_syncToFirebase\(\);\s*\}\,\s*\)\,\s*)(\]\,\s*\)\,\s*\)\,\s*const SizedBox\(height\: 48\)\,\s*SizedBox\(key\: _audioKey\)\,)', content, re.DOTALL)
    if match_video:
        content = content.replace(match_video.group(0), match_video.group(1) + video_block + match_video.group(2))
        print("Injected Video Player block.")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

