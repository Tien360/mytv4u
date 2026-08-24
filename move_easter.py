with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re

# 1. Add Easter Egg SwitchListTile right after ambient_bg SwitchListTile
ambient_block_regex = r"(SwitchListTile\([\s\S]*?ambient_bg[\s\S]*?\}\,\s*\)\,)"
match = re.search(ambient_block_regex, text)
if match:
    ambient_block = match.group(1)
    easter_tile = """
                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            title: Text(L10n.t('easter_eggs_toggle') ?? 'Bật Hiệu ứng Tương tác', style: const TextStyle(color: Colors.white, fontSize: 16)),
                                            subtitle: Text(L10n.t('easter_eggs_desc') ?? 'Nhấn vào dòng trạng thái tập mới ở phim để quay thưởng hiệu ứng! Có 4 bậc từ Phổ thông đến Huyền thoại (1%).', style: const TextStyle(color: Colors.white54, fontSize: 12)),
                                            secondary: const Icon(Icons.celebration, color: Colors.white70),
                                            value: _easterEggsEnabled,
                                            activeColor: Colors.amber,
                                            onChanged: (v) async {
                                              setState(() => _easterEggsEnabled = v);
                                              final p = await SharedPreferences.getInstance();
                                              await p.setBool('enable_easter_eggs', v);
                                            },
                                          ),"""
    text = text.replace(ambient_block, ambient_block + easter_tile)

# 2. Remove the old easter egg block
old_easter_block_regex = r"\s*const SizedBox\(height: 16\);\s*_buildSectionTitle\(\s*Icons\.auto_awesome,\s*L10n\.t\('easter_eggs_title'\) \?\? 'Hieu ung Tuong tac \(Easter Eggs\)',\s*\),\s*const SizedBox\(height: 8\);\s*_buildSettingToggle\([\s\S]*?await p\.setBool\('enable_easter_eggs', v\);\s*\},\s*\),"
text = re.sub(old_easter_block_regex, "", text)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Moved Easter Egg toggle to Health Utilities!")
