import sys
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace _searchController hints and logic
target_hint = """                              hintText: _selectedIndex == 3
                                  ? L10n.t('search_tv') ?? 'Tìm kiếm kênh TV...'
                                  : _selectedIndex == 4
                                  ? L10n.t('search_sports') ??
                                        'Tìm kiếm sự kiện thể thao...'
                                  : L10n.t('search_movies') ?? 'Tìm kiếm phim...',"""
new_hint = """                              hintText: _selectedIndex == 3
                                  ? L10n.t('search_tv') ?? 'Tìm kiếm kênh TV...'
                                  : _selectedIndex == 4
                                  ? L10n.t('search_sports') ?? 'Tìm kiếm sự kiện thể thao...'
                                  : _selectedIndex == 5
                                  ? 'Tìm kiếm trò chơi...'
                                  : L10n.t('search_movies') ?? 'Tìm kiếm phim...',"""
if target_hint in c:
    c = c.replace(target_hint, new_hint)
    print("Fixed hint")
else:
    print("Could not find hint")

# Add _gamingKey
if "_gamingKey" not in c:
    c = c.replace("final GlobalKey<SearchScreenState> _searchKey = GlobalKey();", "final GlobalKey<SearchScreenState> _searchKey = GlobalKey();\n  final GlobalKey<dynamic> _gamingKey = GlobalKey();")
    print("Added _gamingKey")

target_gaming_screen = """      case 5:
        return const GamingScreen();"""
new_gaming_screen = """      case 5:
        return GamingScreen(key: _gamingKey);"""
if target_gaming_screen in c:
    c = c.replace(target_gaming_screen, new_gaming_screen)
    print("Passed _gamingKey to GamingScreen")
else:
    print("Could not find target_gaming_screen")

target_onChanged = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch(query);
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch(query);
                              } else {"""
new_onChanged = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch(query);
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch(query);
                              } else if (_selectedIndex == 5) {
                                _gamingKey.currentState?.performSearch(query);
                              } else {"""
if target_onChanged in c:
    c = c.replace(target_onChanged, new_onChanged)
    print("Fixed onChanged logic")
else:
    print("Could not find onChanged")
    
target_onSubmitted = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch(value);
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch(value);
                              } else {"""
new_onSubmitted = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch(value);
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch(value);
                              } else if (_selectedIndex == 5) {
                                _gamingKey.currentState?.performSearch(value);
                              } else {"""
if target_onSubmitted in c:
    c = c.replace(target_onSubmitted, new_onSubmitted)
    print("Fixed onSubmitted logic")
else:
    print("Could not find onSubmitted")
    
target_clear = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch('');
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch('');
                              } else {"""
new_clear = """                              if (_selectedIndex == 3) {
                                _tvKey.currentState?.performSearch('');
                              } else if (_selectedIndex == 4) {
                                _sportKey.currentState?.performSearch('');
                              } else if (_selectedIndex == 5) {
                                _gamingKey.currentState?.performSearch('');
                              } else {"""
if target_clear in c:
    c = c.replace(target_clear, new_clear)
    print("Fixed clear logic")
else:
    print("Could not find clear")

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
