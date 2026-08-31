import sys, re
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix hintText
c = re.sub(r"hintText: _selectedIndex == 3\s*\?\s*L10n\.t\('search_tv'\).*?\s*: L10n\.t\('search_movies'\)[^,]+,",
    r"hintText: _selectedIndex == 3 ? L10n.t('search_tv') ?? 'Tìm kiếm kênh TV...' : _selectedIndex == 4 ? L10n.t('search_sports') ?? 'Tìm kiếm sự kiện thể thao...' : _selectedIndex == 5 ? 'Tìm kiếm trò chơi...' : L10n.t('search_movies') ?? 'Tìm kiếm phim...',",
    c, flags=re.DOTALL)

# Add _gamingKey
if "_gamingKey" not in c:
    c = re.sub(r"final GlobalKey<SearchScreenState> _searchKey = GlobalKey\(\);",
               r"final GlobalKey<SearchScreenState> _searchKey = GlobalKey();\n  final GlobalKey<dynamic> _gamingKey = GlobalKey();", c)

# Pass key to GamingScreen
c = re.sub(r"case 5:\s*return const GamingScreen\(\);", r"case 5:\n        return GamingScreen(key: _gamingKey);", c)

# Fix onChanged, onSubmitted, clear logic
def fix_search_logic(match):
    return match.group(0).replace(
        "} else {",
        "} else if (_selectedIndex == 5) {\n                                _gamingKey.currentState?.performSearch(" + match.group(1) + ");\n                              } else {"
    )

c = re.sub(r"if \(_selectedIndex == 3\) \{.*?_tvKey\.currentState\?\.performSearch\((.*?)\);.*?_sportKey\.currentState\?\.performSearch\(\1\);.*?\} else \{", fix_search_logic, c, flags=re.DOTALL)

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)

print("updated main_screen")
