import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the control character with the actual string
bad_char = chr(1)
if bad_char in content:
    content = content.replace(bad_char, """if (_getAgeRating() != null)
                                                _buildBadge(
                                                  _getAgeRating()!,
                                                  ['R', 'NC-17', 'TV-MA', '18+'].contains(_getAgeRating()) ? Colors.redAccent : Colors.orangeAccent,
                                                ),""")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed control character!")
else:
    print("Not found.")
