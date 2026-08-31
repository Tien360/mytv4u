import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Spacer for title bar and search bar conditional
pattern_spacer = r"// Spacer for title bar and search bar\s*const SizedBox\(height: 56\),"
repl_spacer = """// Spacer for title bar and search bar
                if (_selectedIndex != 3) const SizedBox(height: 56),"""
content = re.sub(pattern_spacer, repl_spacer, content)

# 2. Global Search Bar conditional
pattern_search_bar = r"(// Global Search Bar[^\n]*\n\s*)AnimatedPositioned\("
repl_search_bar = r"\1if (_selectedIndex != 3) AnimatedPositioned("
content = re.sub(pattern_search_bar, repl_search_bar, content)

# 3. Auto-collapse sidebar when selecting YouTube
pattern_ontap = r"setState\(\(\) \{\s*_selectedIndex = index;\s*\}\);"
repl_ontap = """setState(() {
              _selectedIndex = index;
              if (index == 3) {
                _isSidebarCollapsed = true;
              }
            });"""
content = re.sub(pattern_ontap, repl_ontap, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated layout in main_screen")
