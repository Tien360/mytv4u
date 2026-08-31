import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

if "import '../globals.dart';" not in content:
    content = content.replace("import '../utils/ui_utils.dart';", "import '../utils/ui_utils.dart';\nimport '../globals.dart';")

if 'bool _minimalistUi = false;' not in content:
    content = content.replace('bool _hwAccel = true;', 'bool _hwAccel = true;\n    bool _minimalistUi = false;')

if '_minimalistUi = prefs.getBool' not in content:
    content = content.replace("_hwAccel = prefs.getBool('enable_hw_accel') ?? true;", "_hwAccel = prefs.getBool('enable_hw_accel') ?? true;\n          _minimalistUi = prefs.getBool('minimalist_ui') ?? false;")

content = content.replace("Text(L10n.t('ambient_bg'))", "Text(L10n.t('setting_amb_title') ?? 'Hình nền mờ Ambient')")
content = re.sub(r"const Text\(\s*'Hiện thị hình nền mờ từ poster phim giúp giao diện sống \nđộng hơn',\s*\)", "Text(L10n.t('setting_amb_desc') ?? 'Hiện thị hình nền mờ từ poster phim giúp giao diện sống động hơn', style: const TextStyle(color: Colors.white54, fontSize: 12))", content)

content = content.replace("Text(L10n.t('easter_eggs_toggle') ?? 'Bật Hiệu ứng Tương tác', style: const TextStyle(color: Colors.white, fontSize: 16))", "Text(L10n.t('setting_egg_title') ?? 'Bật Hiệu ứng Tương tác', style: const TextStyle(color: Colors.white, fontSize: 16))")
content = content.replace("Text(L10n.t('easter_eggs_desc') ?? 'Nhấn vào dòng trạng thái tập mới ở phim để quay thưởng hiệu ứng! Có 4 bậc từ Phổ thông đến Huyền thoại (1%).', style: const TextStyle(color: Colors.white54, fontSize: 12))", "Text(L10n.t('setting_egg_desc') ?? 'Nhấn vào dòng trạng thái tập mới ở phim để quay thưởng hiệu ứng! Có 4 bậc từ Phổ thông đến Huyền thoại (1%).', style: const TextStyle(color: Colors.white54, fontSize: 12))")

min_ui_block = """                                      const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            title: Text(L10n.t('setting_min_title') ?? 'Giao diện tối giản (Máy yếu)', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            subtitle: Text(L10n.t('setting_min_desc') ?? 'Tắt các hiệu ứng gương kính (kính mờ), giúp app chạy cực nhẹ trên máy tính cũ', style: const TextStyle(color: Colors.white54, fontSize: 12)),
                                            value: _minimalistUi,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setBool('minimalist_ui', val);
                                              isMinimalistUi.value = val;
                                              setState(() {
                                                _minimalistUi = val;
                                              });
                                            },
                                          ),
"""
if 'setting_min_title' not in content:
    content = content.replace("                                      const Divider(color: Colors.white12),\n                                          SwitchListTile(\n                                            title: Text(L10n.t('setting_amb_title')", min_ui_block + "                                      const Divider(color: Colors.white12),\n                                          SwitchListTile(\n                                            title: Text(L10n.t('setting_amb_title')")

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched!")
