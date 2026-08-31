import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\models\movie.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Episode class definition
old_ep_class = """class Episode {
  final String name;
  final String slug;
  final String m3u8Url;
  final String embedUrl;

  Episode({
    required this.name,
    required this.slug,
    required this.m3u8Url,
    required this.embedUrl,
  });"""

new_ep_class = """class Episode {
  final String name;
  final String slug;
  final String m3u8Url;
  final String embedUrl;
  final String? filename;

  Episode({
    required this.name,
    required this.slug,
    required this.m3u8Url,
    required this.embedUrl,
    this.filename,
  });"""

content = content.replace(old_ep_class, new_ep_class)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Episode model in movie.dart")
