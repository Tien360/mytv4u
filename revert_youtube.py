import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove YoutubeScreen from _screens
content = re.sub(
    r"\s*const YoutubeScreen\(key: PageStorageKey\('YoutubeScreen'\)\),",
    "",
    content
)

# 2. Remove YouTube from sidebar and fix subsequent indices
content = re.sub(
    r"\s*_buildNavItem\(\s*Icons\.smart_display_outlined,\s*Icons\.smart_display,\s*'YouTube',\s*3,\s*\),\s*const SizedBox\(height: 8\),",
    "",
    content
)
content = content.replace("'TV', 4", "'TV', 3")
content = content.replace("Th\u1ec3 Thao', 5", "Th\u1ec3 Thao', 4")
content = content.replace("'Th\u01b0 vi\u1ec7n', 6", "'Th\u01b0 vi\u1ec7n', 5")

# 3. Fix _searchController logic (indices 4, 5 -> 3, 4)
content = content.replace("if (_selectedIndex == 4)", "if (_selectedIndex == 3)")
content = content.replace("else if (_selectedIndex == 4)", "else if (_selectedIndex == 3)")
content = content.replace("if (_selectedIndex == 5)", "if (_selectedIndex == 4)")
content = content.replace("else if (_selectedIndex == 5)", "else if (_selectedIndex == 4)")

# 4. Fix hintText indices
content = content.replace("hintText: _selectedIndex == 4", "hintText: _selectedIndex == 3")
content = content.replace(": _selectedIndex == 5", ": _selectedIndex == 4")

# 5. Revert layout conditionals
content = re.sub(
    r"if \(_selectedIndex != 3\) const SizedBox\(height: 56\),",
    "const SizedBox(height: 56),",
    content
)
content = re.sub(
    r"if \(_selectedIndex != 3\) AnimatedPositioned\(",
    "AnimatedPositioned(",
    content
)

# 6. Revert auto-collapse in _buildNavItem
pattern_ontap = r"setState\(\(\) \{\s*_selectedIndex = index;\s*if \(index == 3\) \{\s*_isSidebarCollapsed = true;\s*\}\s*\}\);"
repl_ontap = """setState(() {
                _selectedIndex = index;
              });"""
content = re.sub(pattern_ontap, repl_ontap, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted YouTube tab in main_screen")
