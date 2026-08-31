with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _videoKey
keys_search = "final GlobalKey _audioKey = GlobalKey();"
keys_replace = """final GlobalKey _audioKey = GlobalKey();
  final GlobalKey _videoKey = GlobalKey();"""
idx2 = content.find(keys_search)
if idx2 != -1:
    content = content[:idx2] + keys_replace + content[idx2+len(keys_search):]
    print("Injected _videoKey")

# 2. Add to sidebar
sidebar_search = """        _buildSidebarItem(
          L10n.t('health_utilities') ?? 'Hệ thống',
          Icons.settings_suggest,
          _systemKey,
        ),"""
sidebar_replace = sidebar_search + """
        _buildSidebarItem(
          L10n.t('player_settings') ?? 'Trình phát Phim',
          Icons.play_circle_filled,
          _videoKey,
        ),
        _buildSidebarItem(
          L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
          Icons.music_note,
          _audioKey,
        ),"""
idx3 = content.find(sidebar_search)
if idx3 != -1:
    content = content[:idx3] + sidebar_replace + content[idx3+len(sidebar_search):]
    print("Injected Sidebar items")
else:
    # Try just 'health_utilities'
    print("Could not find sidebar search!")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
