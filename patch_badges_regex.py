import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r"if \(_premiumServers\.isNotEmpty\)\s+_buildBadge\(\s+'Premium TM - Vietsub',\s+Colors\.blueAccent,\s+\),")

new_str = """if (_premiumServers.isNotEmpty)
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

if pattern.search(content):
    content = pattern.sub(new_str, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced via regex successfully.")
else:
    print("Regex failed to match.")
