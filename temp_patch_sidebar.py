import sys

with open("lib/screens/main_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

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

# Using regex or simpler replace
import re
content = re.sub(
    r"(\s*)_buildNavItem\(\s*Icons\.folder_outlined,\s*Icons\.folder,\s*L10n\.t\('nav_library'\) \?\? 'Thư viện',\s*5,\s*\),",
    r"\1_buildNavItem(\n\1  Icons.videogame_asset_outlined,\n\1  Icons.videogame_asset,\n\1  L10n.t('nav_gaming') ?? 'Trò chơi',\n\1  5,\n\1),\n\1const SizedBox(height: 8),\n\1_buildNavItem(\n\1  Icons.folder_outlined,\n\1  Icons.folder,\n\1  L10n.t('nav_library') ?? 'Thư viện',\n\1  6,\n\1),",
    content
)

with open("lib/screens/main_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched main_screen")
