import os
import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update _buildSidebarMenu
new_menu = '''
  Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(L10n.t('sync_account') ?? 'Tài khoản', Icons.account_circle, _accountKey),
        _buildSidebarItem(L10n.t('health_utilities') ?? 'Hệ thống', Icons.settings_suggest, _systemKey),
        _buildSidebarItem(L10n.t('sources') ?? 'Nguồn phim', Icons.source, _sourcesKey),
        _buildSidebarItem(L10n.t('global_color_settings') ?? 'Màu sắc', Icons.color_lens, _colorKey),
        _buildSidebarItem(L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles, _subtitleKey),
        _buildSidebarItem(L10n.t('info_contact') ?? 'Thông tin', Icons.info_outline, _infoKey),
      ],
    );
  }
'''

text = re.sub(r'Widget _buildSidebarMenu\(\) \{[\s\S]*?\];\n  \}', new_menu.strip(), text)

# Now we need to rearrange the sections in the body.
# They are currently in this order:
# 1. Account
# 2. Color
# 3. Subtitles
# 4. System
# 5. Sources
# 6. Info

# Let's extract the exact blocks for each section.
# We'll split the content inside children: [ of the ConstrainedBox's Column.
# We can find each block by its SizedBox(key: ...)

# We need to make sure we don't mess up the braces.
# I'll just use a regex for each block.

block_account = re.search(r'(SizedBox\(key: _accountKey\),[\s\S]*?)(?=SizedBox\(key: _colorKey\),)', text).group(1)
block_color = re.search(r'(SizedBox\(key: _colorKey\),[\s\S]*?)(?=SizedBox\(key: _subtitleKey\),)', text).group(1)
block_subtitle = re.search(r'(SizedBox\(key: _subtitleKey\),[\s\S]*?)(?=SizedBox\(key: _systemKey\),)', text).group(1)
block_system = re.search(r'(SizedBox\(key: _systemKey\),[\s\S]*?)(?=SizedBox\(key: _sourcesKey\),)', text).group(1)
block_sources = re.search(r'(SizedBox\(key: _sourcesKey\),[\s\S]*?)(?=SizedBox\(key: _infoKey\),)', text).group(1)
block_info = re.search(r'(SizedBox\(key: _infoKey\),[\s\S]*?)(?=\s*const SizedBox\(height: 64\), // Extra bottom padding)', text).group(1)

# Now replace the whole block from _accountKey to the end of info block with the new order.
new_order = block_account + block_system + block_sources + block_color + block_subtitle + block_info

text = re.sub(r'SizedBox\(key: _accountKey\),[\s\S]*?(?=\s*const SizedBox\(height: 64\), // Extra bottom padding)', new_order, text)

# Fix the Scrolling issue: Add alignment: 0.0 or 0.1 so it's slightly below the top (in case of headers).
text = text.replace('Scrollable.ensureVisible(\n        key.currentContext!,', 'Scrollable.ensureVisible(\n        key.currentContext!,\n        alignment: 0.1, // Offset from top')


with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done")
