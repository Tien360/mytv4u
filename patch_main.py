import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add import
if "import 'youtube_screen.dart';" not in content:
    content = content.replace("import 'sport_screen.dart';", "import 'sport_screen.dart';\nimport 'youtube_screen.dart';")

# 2. Update _screens list (Insert YoutubeScreen at index 3)
screens_orig = """      SearchScreen(key: _searchKey),
      TvScreen(key: _tvKey),
      SportScreen(key: _sportKey),
      const LibraryScreen(key: PageStorageKey('LibraryScreen')),"""
screens_new = """      SearchScreen(key: _searchKey),
      const YoutubeScreen(key: PageStorageKey('YoutubeScreen')),
      TvScreen(key: _tvKey),
      SportScreen(key: _sportKey),
      const LibraryScreen(key: PageStorageKey('LibraryScreen')),"""
content = content.replace(screens_orig, screens_new)

# 3. Update Sidebar Nav Items
nav_orig = """                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.live_tv_outlined,
                            Icons.live_tv,
                            L10n.t('nav_tv'),
                            3,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.sports_soccer_outlined,
                            Icons.sports_soccer,
                            L10n.t('nav_sport'),
                            4,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.video_library_outlined,
                            Icons.video_library,
                            L10n.t('nav_library'),
                            5,
                          ),"""
nav_new = """                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.smart_display_outlined,
                            Icons.smart_display,
                            'YouTube',
                            3,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.live_tv_outlined,
                            Icons.live_tv,
                            L10n.t('nav_tv'),
                            4,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.sports_soccer_outlined,
                            Icons.sports_soccer,
                            L10n.t('nav_sport'),
                            5,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.video_library_outlined,
                            Icons.video_library,
                            L10n.t('nav_library'),
                            6,
                          ),"""
content = content.replace(nav_orig, nav_new)

# 4. Fix _selectedIndex checks in search bar (shift 3->4, 4->5)
content = re.sub(r"_selectedIndex == 3", r"_selectedIndex == 4", content)
content = re.sub(r"_selectedIndex == 4", r"_selectedIndex == 5", content)
# Wait, this might replace the already replaced "4" to "5"!
# Let's write a python function to safely shift.
