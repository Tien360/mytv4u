# 1. Wrap logo with GestureDetector for double-tap
import re

with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Add import for NextEpisodeTracker if not there
if "next_episode_tracker" not in text:
    text = text.replace("import 'package:cached_network_image/cached_network_image.dart';",
                        "import 'package:cached_network_image/cached_network_image.dart';\nimport '../widgets/next_episode_tracker.dart';")

# Wrap logo Image.asset with GestureDetector double-tap
old_logo = "Image.asset('assets/logo.png', height: 48),"
new_logo = """GestureDetector(
              onDoubleTap: () => NextEpisodeTracker.triggerLegendaryFromOutside(context),
              child: Image.asset('assets/logo.png', height: 48),
            ),"""
text = text.replace(old_logo, new_logo)

# 2. Find a good place to insert the Easter Egg toggle (after health_utilities section or before restore_default)
# Find "watch_limit" setting area and insert after it
egg_toggle_code = """
                                    const SizedBox(height: 16),
                                    _buildSectionTitle(
                                      Icons.auto_awesome,
                                      L10n.t('easter_eggs_title') ?? 'Hieu ung Tuong tac (Easter Eggs)',
                                    ),
                                    const SizedBox(height: 8),
                                    _buildSettingToggle(
                                      icon: Icons.celebration,
                                      title: L10n.t('easter_eggs_toggle') ?? 'Bat Hieu ung Trung Phuc Sinh',
                                      subtitle: L10n.t('easter_eggs_desc') ?? 'Nhan vao dong trang thai tap moi o moi phim de quay thuong hieu ung! Co 4 bac tu Pho thong den Huyen thoai (1%). Chuc ban may man!',
                                      value: _easterEggsEnabled,
                                      onChanged: (v) async {
                                        setState(() => _easterEggsEnabled = v);
                                        final p = await SharedPreferences.getInstance();
                                        await p.setBool('enable_easter_eggs', v);
                                      },
                                    ),"""

# Insert before restore_default section
text = text.replace(
    "SizedBox(key: _infoKey),",
    egg_toggle_code + "\n                                    SizedBox(key: _infoKey),"
)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Settings updated!")
