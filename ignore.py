with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
pattern = r"Widget _buildSettingToggle\(\{[\s\S]*?\}\) \{[\s\S]*?return GlassContainer\([\s\S]*?\}\,\s*\)\,[\s\S]*?\}\,\s*\)\,[\s\S]*?\]\,\s*\)\,[\s\S]*?\]\,\s*\)\,[\s\S]*?\}\n"
# Actually, it's simpler to just leave the unused function there, but let's remove it safely.
# No, Dart compiler doesn't care much if a private widget builder is unused (it might give a warning). Let's leave it to avoid breaking braces.
