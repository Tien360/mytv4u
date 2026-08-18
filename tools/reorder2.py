import os
import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject missing keys
if 'SizedBox(key: _systemKey)' not in text:
    text = text.replace("_buildSectionTitle(Icons.health_and_safety, L10n.t('health_utilities')),", "SizedBox(key: _systemKey),\n                          _buildSectionTitle(Icons.health_and_safety, L10n.t('health_utilities')),")

if 'SizedBox(key: _sourcesKey)' not in text:
    text = text.replace("_buildSectionTitle(Icons.source, L10n.t('movie_sources')),", "SizedBox(key: _sourcesKey),\n                              _buildSectionTitle(Icons.source, L10n.t('movie_sources')),")

# 2. Extract blocks
block_account = re.search(r'(SizedBox\(key: _accountKey\),[\s\S]*?)(?=SizedBox\(key: _colorKey\),)', text).group(1)
block_color = re.search(r'(SizedBox\(key: _colorKey\),[\s\S]*?)(?=SizedBox\(key: _subtitleKey\),)', text).group(1)
block_subtitle = re.search(r'(SizedBox\(key: _subtitleKey\),[\s\S]*?)(?=SizedBox\(key: _systemKey\),)', text).group(1)
block_system = re.search(r'(SizedBox\(key: _systemKey\),[\s\S]*?)(?=SizedBox\(key: _sourcesKey\),)', text).group(1)
block_sources = re.search(r'(SizedBox\(key: _sourcesKey\),[\s\S]*?)(?=SizedBox\(key: _infoKey\),)', text).group(1)

# Now replace the whole block from _accountKey to the end of info block with the new order.
new_order = block_account + block_system + block_sources + block_color + block_subtitle

text = re.sub(r'SizedBox\(key: _accountKey\),[\s\S]*?(?=SizedBox\(key: _infoKey\),)', new_order, text)

# Fix the Scrolling issue: offset alignment
text = text.replace('Scrollable.ensureVisible(\n        key.currentContext!,', 'Scrollable.ensureVisible(\n        key.currentContext!,\n        alignment: 0.0, // Top align')

# Sidebar Menu update
new_menu = '''
  Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(L10n.t('sync_account'), Icons.account_circle, _accountKey),
        _buildSidebarItem(L10n.t('health_utilities'), Icons.health_and_safety, _systemKey),
        _buildSidebarItem(L10n.t('movie_sources'), Icons.source, _sourcesKey),
        _buildSidebarItem(L10n.t('global_color_settings'), Icons.color_lens, _colorKey),
        _buildSidebarItem(L10n.t('subtitles'), Icons.subtitles, _subtitleKey),
        _buildSidebarItem(L10n.t('info_contact'), Icons.info_outline, _infoKey),
      ],
    );
  }
'''
text = re.sub(r'Widget _buildSidebarMenu\(\) \{[\s\S]*?\];\n  \}', new_menu.strip(), text)


with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done")
