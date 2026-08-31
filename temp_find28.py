with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find("          // YouTube")
end_idx = content.find("  Widget _buildSettingToggle({")
if start_idx != -1 and end_idx != -1:
    print(f"Start: {start_idx}, End: {end_idx}")
    print(repr(content[end_idx-50:end_idx]))
