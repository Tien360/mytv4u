import sys

with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Add performSearch logic
target_list = """class _GamingScreenState extends State<GamingScreen> {
  final List<Map<String, String>> _games = ["""
new_list = """class _GamingScreenState extends State<GamingScreen> {
  String _searchQuery = '';
  
  void performSearch(String query) {
    if (!mounted) return;
    setState(() {
      _searchQuery = query.toLowerCase();
    });
  }

  final List<Map<String, String>> _games = ["""

if target_list in c:
    c = c.replace(target_list, new_list)
else:
    print("Could not find _games list")

target_itemCount = """              itemCount: _games.length,"""
new_itemCount = """              itemCount: _games.where((g) => g['title']!.toLowerCase().contains(_searchQuery)).length,"""
if target_itemCount in c:
    c = c.replace(target_itemCount, new_itemCount)
else:
    print("Could not find itemCount")

target_itemBuilder = """              itemBuilder: (context, index) {
                final game = _games[index];"""
new_itemBuilder = """              itemBuilder: (context, index) {
                final filteredGames = _games.where((g) => g['title']!.toLowerCase().contains(_searchQuery)).toList();
                final game = filteredGames[index];"""
if target_itemBuilder in c:
    c = c.replace(target_itemBuilder, new_itemBuilder)
else:
    print("Could not find itemBuilder")

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated gaming_screen search logic")
