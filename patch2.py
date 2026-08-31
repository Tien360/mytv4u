import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix _openInWebPlayer to use embed URL
search_func = """      String targetUrl = widget.lazyPlaylistUrl ?? _currentUrl;"""
new_func = """      String targetUrl = widget.lazyPlaylistUrl ?? _currentUrl;
      
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
if "https://www.youtube.com/embed/$vid?autoplay=1" not in content:
    content = content.replace(search_func, new_func)

# Add button safely using regex
pattern = r"(\s*)(// Settings Gear Button)"
replacement = r"""\1// Web Player Button (YouTube 4K+)
\1if (_isYoutube && _ytQualities.any((q) => q >= 2160)) ...[
\1  IconButton(
\1    icon: const Icon(
\1      Icons.open_in_browser,
\1      color: Colors.white,
\1      size: 20,
\1    ),
\1    onPressed: _openInWebPlayer,
\1    tooltip: 'Phát bằng trình duyệt (Tối ưu 4K/8K)',
\1    padding: const EdgeInsets.all(4),
\1    constraints: const BoxConstraints(),
\1  ),
\1  const SizedBox(width: 10),
\1]
\1\2"""
if "Icons.open_in_browser" not in content:
    content = re.sub(pattern, replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen.dart")
