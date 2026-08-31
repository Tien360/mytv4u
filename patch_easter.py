import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _easterEggsEnabled and _isFinancialExpanded
if "bool _isFinancialExpanded = false;" not in content:
    content = content.replace("bool _autoPlayTrailerSetting = true;", "bool _autoPlayTrailerSetting = true;\n  bool _easterEggsEnabled = true;\n  bool _isFinancialExpanded = false;")

# 2. Add it to _loadSettings
load_settings_old = """        setState(() {
          _autoPlayTrailerSetting = prefs.getBool('auto_play_trailer') ?? true;
        });"""
load_settings_new = """        setState(() {
          _autoPlayTrailerSetting = prefs.getBool('auto_play_trailer') ?? true;
          _easterEggsEnabled = prefs.getBool('enable_easter_eggs') ?? true;
        });"""
content = content.replace(load_settings_old, load_settings_new)

# 3. Replace the caller of _buildFinancialBox
caller_old = """if (_tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0 && _tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0) ...[
                                              const SizedBox(height: 24),
                                              _buildFinancialBox(_tmdbDetails!['budget'], _tmdbDetails!['revenue']),
                                            ],"""
caller_new = """if (_easterEggsEnabled && _tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0 && _tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0) ...[
                                              const SizedBox(height: 16),
                                              _buildFinancialBox(_tmdbDetails!['budget'], _tmdbDetails!['revenue']),
                                            ],"""
content = content.replace(caller_old, caller_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated load settings and caller")
