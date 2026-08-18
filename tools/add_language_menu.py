import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add _languageKey
if '_languageKey = GlobalKey();' not in text:
    text = text.replace('final _subtitleKey = GlobalKey();', 'final _subtitleKey = GlobalKey();\n  final _languageKey = GlobalKey();')

# 2. Add language to sidebar menu. The user wants it on the sidebar. I'll put it after System.
old_menu = '''  Widget _buildSidebarMenu() {
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
  }'''

new_menu = '''  Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(L10n.t('sync_account') ?? 'Tài khoản', Icons.account_circle, _accountKey),
        _buildSidebarItem(L10n.t('health_utilities') ?? 'Hệ thống', Icons.settings_suggest, _systemKey),
        _buildSidebarItem(L10n.t('language_settings') ?? 'Ngôn ngữ', Icons.language, _languageKey),
        _buildSidebarItem(L10n.t('sources') ?? 'Nguồn phim', Icons.source, _sourcesKey),
        _buildSidebarItem(L10n.t('global_color_settings') ?? 'Màu sắc', Icons.color_lens, _colorKey),
        _buildSidebarItem(L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles, _subtitleKey),
        _buildSidebarItem(L10n.t('info_contact') ?? 'Thông tin', Icons.info_outline, _infoKey),
      ],
    );
  }'''

text = text.replace(old_menu, new_menu)

# 3. Add SizedBox(key: _languageKey) to the body.
# It is currently located around _buildSectionTitle(Icons.language, L10n.t('language_settings'))
if 'SizedBox(key: _languageKey)' not in text:
    text = text.replace("_buildSectionTitle(Icons.language, L10n.t('language_settings')),", "SizedBox(key: _languageKey),\n                          _buildSectionTitle(Icons.language, L10n.t('language_settings')),")

# 4. Now we need to move the language block to right after system block.
# Let's extract everything inside the Column of the body.
# Wait, Language is part of the children list. Instead of regexing the whole block (which can be fragile), 
# I will use a simple split/rejoin or regex on the blocks.
# Block order in body currently: Account, System, Sources, Color, Subtitles, Language, Info.
# We want: Account, System, Language, Sources, Color, Subtitles, Info.

block_account = re.search(r'(SizedBox\(key: _accountKey\),[\s\S]*?)(?=SizedBox\(key: _systemKey\),)', text).group(1)
block_system = re.search(r'(SizedBox\(key: _systemKey\),[\s\S]*?)(?=SizedBox\(key: _sourcesKey\),)', text).group(1)
block_sources = re.search(r'(SizedBox\(key: _sourcesKey\),[\s\S]*?)(?=SizedBox\(key: _colorKey\),)', text).group(1)
block_color = re.search(r'(SizedBox\(key: _colorKey\),[\s\S]*?)(?=SizedBox\(key: _subtitleKey\),)', text).group(1)
block_subtitle = re.search(r'(SizedBox\(key: _subtitleKey\),[\s\S]*?)(?=SizedBox\(key: _languageKey\),)', text).group(1)
block_language = re.search(r'(SizedBox\(key: _languageKey\),[\s\S]*?)(?=SizedBox\(key: _infoKey\),)', text).group(1)

new_order = block_account + block_system + block_language + block_sources + block_color + block_subtitle

text = re.sub(r'SizedBox\(key: _accountKey\),[\s\S]*?(?=SizedBox\(key: _infoKey\),)', new_order, text)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Settings screen updated")
