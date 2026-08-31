import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# I will just replace the whole _buildSidebarMenu()
new_sidebar = """  Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(
          L10n.t('sync_account') ?? 'Tài khoản',
          Icons.account_circle,
          _accountKey,
        ),
        _buildSidebarItem(
          L10n.t('health_utilities') ?? 'Hệ thống',
          Icons.settings_suggest,
          _systemKey,
        ),
        _buildSidebarItem(
          L10n.t('language_settings') ?? 'Ngôn ngữ',
          Icons.language,
          _languageKey,
        ),
        _buildSidebarItem(
          L10n.t('player_settings') ?? 'Trình phát Phim',
          Icons.play_circle_filled,
          _videoKey,
        ),
        _buildSidebarItem(
          L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
          Icons.music_note,
          _audioKey,
        ),
        _buildSidebarItem(
          L10n.t('sources') ?? 'Nguồn phim',
          Icons.source,
          _sourcesKey,
        ),
        _buildSidebarItem(
          L10n.t('global_color_settings') ?? 'Màu sắc',
          Icons.color_lens,
          _colorKey,
        ),
        _buildSidebarItem(
          L10n.t('subtitles') ?? 'Phụ đề',
          Icons.subtitles,
          _subtitleKey,
        ),
        _buildSidebarItem(
          L10n.t('keyboard_shortcuts') ?? 'Phím tắt',
          Icons.keyboard,
          _shortcutsKey,
        ),
        _buildSidebarItem(
          L10n.t('info_contact') ?? 'Thông tin',
          Icons.info_outline,
          _infoKey,
        ),
      ],
    );
  }"""

import re
match = re.search(r'Widget _buildSidebarMenu\(\) \{.*?\n  \}', content, re.DOTALL)
if match:
    content = content[:match.start()] + new_sidebar + content[match.end():]
    print("Replaced sidebar!")
else:
    print("Could not find sidebar")
    
with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
