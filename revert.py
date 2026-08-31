import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Undo embed patch
search_func = """      String targetUrl = widget.lazyPlaylistUrl ?? _currentUrl;
      
      // If YouTube, use embed to hide comments/sidebar and play cleanly
      if (targetUrl.contains('youtube.com') || targetUrl.contains('youtu.be')) {
        String? vid;
        if (targetUrl.contains('v=')) {
          final uri = Uri.parse(targetUrl);
          vid = uri.queryParameters['v'];
        } else if (targetUrl.contains('youtu.be/')) {
          vid = targetUrl.split('youtu.be/').last.split('?').first;
        }
        if (vid != null) {
          targetUrl = "https://www.youtube.com/embed/$vid?autoplay=1";
        }
      }"""
new_func = """      String targetUrl = widget.lazyPlaylistUrl ?? _currentUrl;"""
if search_func in content:
    content = content.replace(search_func, new_func)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted embed patch")
