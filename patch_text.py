import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_button = """children: _currentServer!.items.asMap().entries.map((entry) {
          final index = entry.key;
          final ep = entry.value;
          return HoverEpisodeButton(
            text: ep.name,"""

new_button = """children: _currentServer!.items.asMap().entries.map((entry) {
          final index = entry.key;
          final ep = entry.value;
          
          String dispName = ep.name;
          if (ep.filename != null && ep.filename!.isNotEmpty) {
            var q = _parseQualityFromFilename(ep.filename!);
            List<String> tags = [];
            if (q['hdr']!.isNotEmpty) tags.add(q['hdr']!);
            if (q['audio']!.isNotEmpty) tags.add(q['audio']!);
            if (tags.isNotEmpty) {
              dispName += ' • ${tags.join(' ')}';
            }
          }
          
          return HoverEpisodeButton(
            text: dispName,"""

content = content.replace(old_button, new_button)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HoverEpisodeButton text")
