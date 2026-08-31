import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

# Add _videoKey
content = content.replace('final GlobalKey _sourcesKey = GlobalKey();', 'final GlobalKey _sourcesKey = GlobalKey();\n  final GlobalKey _videoKey = GlobalKey();')

# Fix Sidebar Order
sidebar_code = '''    Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(L10n.t('sync_account') ?? 'Tài khoản', Icons.account_circle, _accountKey),
        _buildSidebarItem(L10n.t('health_utilities') ?? 'Hệ thống', Icons.settings_suggest, _systemKey),
        _buildSidebarItem(L10n.t('language_settings') ?? 'Ngôn ngữ', Icons.language, _languageKey),
        _buildSidebarItem(L10n.t('sources') ?? 'Nguồn phim', Icons.source, _sourcesKey),
        _buildSidebarItem(L10n.t('video_player') ?? 'Trình phát Video', Icons.play_circle_outline, _videoKey),
        _buildSidebarItem(L10n.t('audio_player_title') ?? 'Trình phát Nhạc', Icons.library_music, _audioKey),
        _buildSidebarItem(L10n.t('global_color_settings') ?? 'Màu sắc', Icons.color_lens, _colorKey),
        _buildSidebarItem(L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles, _subtitleKey),
        _buildSidebarItem(L10n.t('keyboard_shortcuts') ?? 'Phím tắt', Icons.keyboard, _shortcutsKey),
        _buildSidebarItem(L10n.t('info_contact') ?? 'Thông tin', Icons.info_outline, _infoKey),
      ],
    );
  }'''

# Replace the entire old _buildSidebarMenu()
old_sidebar = re.search(r'Widget _buildSidebarMenu\(\) \{.*?\n  \}', content, flags=re.DOTALL).group(0)
content = content.replace(old_sidebar, sidebar_code)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
