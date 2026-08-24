with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Check if _easterEggsEnabled state var exists
if "_easterEggsEnabled" not in text:
    # Add state variable after other bools
    text = text.replace("bool _isLoggingIn = false;", "bool _isLoggingIn = false;\n  bool _easterEggsEnabled = true;")

# Check if _buildSettingToggle exists already
if "_buildSettingToggle" not in text:
    # Add it before the closing brace of the class (before last })
    # We add it before _buildAppInfoCard
    toggle_method = """
  Widget _buildSettingToggle({required IconData icon, required String title, required String subtitle, required bool value, required ValueChanged<bool> onChanged}) {
    return GlassContainer(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      borderRadius: 12,
      child: Row(
        children: [
          Icon(icon, color: Colors.white70, size: 22),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 14)),
            const SizedBox(height: 4),
            Text(subtitle, style: const TextStyle(color: Colors.white54, fontSize: 12)),
          ])),
          Switch(value: value, onChanged: onChanged, activeColor: Colors.amber),
        ],
      ),
    );
  }

"""
    text = text.replace("  Widget _buildAppInfoCard()", toggle_method + "  Widget _buildAppInfoCard()")

# Load _easterEggsEnabled in _loadSettings
if "enable_easter_eggs" not in text:
    text = text.replace(
        "_prefs = await SharedPreferences.getInstance();",
        "_prefs = await SharedPreferences.getInstance();\n    _easterEggsEnabled = _prefs!.getBool(\"enable_easter_eggs\") ?? true;"
    )

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("All settings fixes applied!")
