import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import_str = "import '../globals.dart';"
if "import '../globals.dart';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport '../globals.dart';")

search = """                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            title: Text(L10n.t('easter_eggs_toggle') ?? 'Bật Hiệu ứng Tương tác', style: const TextStyle(color: Colors.white, fontSize: 16)),"""

replace = """                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            title: Text(L10n.t('setting_min_title') ?? 'Giao diện tối giản (Máy yếu)', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            subtitle: Text(L10n.t('opt_apply_min') ?? 'Bật Giao diện tối giản (Tắt 100% hiệu ứng kính mờ/gương)', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                                            secondary: const Icon(Icons.flash_on, color: Colors.amber),
                                            value: isMinimalistUi.value,
                                            activeColor: Colors.amber,
                                            onChanged: (v) async {
                                              final p = await SharedPreferences.getInstance();
                                              await p.setBool('minimalist_ui', v);
                                              isMinimalistUi.value = v;
                                              setState(() {});
                                              _syncToFirebase();
                                            },
                                          ),
                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            title: Text(L10n.t('easter_eggs_toggle') ?? 'Bật Hiệu ứng Tương tác', style: const TextStyle(color: Colors.white, fontSize: 16)),"""

if search in content:
    content = content.replace(search, replace)
    print("Injected Minimalist toggle!")
else:
    print("Could not find insertion point!")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
