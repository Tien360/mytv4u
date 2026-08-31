import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = """                                              if (_premiumServers.isNotEmpty)
                                                _buildBadge(
                                                  'Premium TM - Vietsub',
                                                  Colors.blueAccent,
                                                ),"""

new_str = """                                              if (_premiumServers.isNotEmpty)
                                                _buildBadge(
                                                  'Premium TM - Vietsub',
                                                  Colors.blueAccent,
                                                ),
                                              if (_movie!.quality.isNotEmpty)
                                                _buildBadge(
                                                  _movie!.quality,
                                                  Colors.greenAccent,
                                                ),
                                              if (_getAgeRating() != null)
                                                _buildBadge(
                                                  _getAgeRating()!,
                                                  ['R', 'NC-17', 'TV-MA', '18+'].contains(_getAgeRating()) ? Colors.redAccent : Colors.orangeAccent,
                                                ),"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced badges successfully.")
else:
    print("Could not find the exact string to replace.")
