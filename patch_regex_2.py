import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

bad_str = """if (uri != null) {
              String rawId = uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '');
              if (rawId.isNotEmpty) {"""

good_str = """String rawId = uri != null ? (uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '')) : '';
            if (rawId.isNotEmpty) {"""

content = content.replace(bad_str, good_str)
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed nesting in movie_detail_screen")
