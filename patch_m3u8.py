import re
with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"static String _processM3u8Url\(String url\) \{[\s\S]*?return url;\s*\}"

new_func = '''static String _processM3u8Url(String url) {
    if (url.isEmpty) return url;
    if (url.contains('workers.dev') ||
        (url.contains('dpdns.org') && !url.contains('stream/hls'))) {
      final rawId = url.split('/').last;
      return 'premium://play/$rawId';
    }
    return url;
  }'''

text, count = re.subn(pattern, new_func, text)
print(f"Replaced {count} times")
with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(text)
