import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

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

match_opt = re.search(r'(                                          ListTile\(\s*title: Text\(\s*L10n.t\(\'watch_limit\'\),)', content)

# Instead of regex, find index!
idx = content.find("ListTile(\n                                      title: Text(\n                                        L10n.t('watch_limit')")
if idx != -1:
    content = content[:idx] + opt_block + content[idx:]
    if "import '../widgets/optimizer_dialog.dart';" not in content:
        content = content.replace("import '../widgets/custom_title_bar.dart';", "import '../widgets/custom_title_bar.dart';\nimport '../widgets/optimizer_dialog.dart';")
    print("Injected Optimizer block.")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
