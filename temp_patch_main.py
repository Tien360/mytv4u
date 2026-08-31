import sys

# 1. READ main_screen.dart
with open("lib/screens/main_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# ADD GAMING SCREEN TO _screens
old_screens = "SportScreen(key: _sportKey),"
new_screens = "SportScreen(key: _sportKey),\n      const GamingScreen(key: PageStorageKey('GamingScreen')),"
content = content.replace(old_screens, new_screens)

# ADD SIDEBAR ITEM
old_sidebar = """                          _buildNavItem(
                            Icons.folder_outlined,
                            Icons.folder,
                            L10n.t('nav_library') ?? 'Thư viện',
                            5,
                          ),"""
new_sidebar = """                          _buildNavItem(
                            Icons.videogame_asset_outlined,
                            Icons.videogame_asset,
                            L10n.t('nav_gaming') ?? 'Trò chơi',
                            5,
                          ),
                          const SizedBox(height: 8),
                          _buildNavItem(
                            Icons.folder_outlined,
                            Icons.folder,
                            L10n.t('nav_library') ?? 'Thư viện',
                            6,
                          ),"""
content = content.replace(old_sidebar, new_sidebar)

# ADD IMPORT
import_gaming = "import 'gaming_screen.dart';"
if import_gaming not in content:
    content = content.replace("import 'library_screen.dart';", "import 'library_screen.dart';\nimport 'gaming_screen.dart';")

with open("lib/screens/main_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated main_screen.dart")
