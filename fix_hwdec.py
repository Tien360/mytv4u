import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: yt-dlp --no-playlist
search_fetch = """      final res = await Process.run(exePath, ['-J', url]);"""
new_fetch = """      final res = await Process.run(exePath, ['--no-playlist', '-J', url]);"""
if "['--no-playlist', '-J', url]" not in content:
    content = content.replace(search_fetch, new_fetch)

# Fix 2: hwdec auto-safe
search_hwdec = """      // Tối ưu tốc độ tải luồng HLS/m3u8 (giảm độ trễ ban đầu)
      try {
        final platform = player.platform as dynamic;
        platform.setProperty('cache', 'yes');"""
new_hwdec = """      // Tối ưu tốc độ tải luồng HLS/m3u8 (giảm độ trễ ban đầu)
      try {
        final platform = player.platform as dynamic;
        platform.setProperty('hwdec', _hwAccel ? 'auto' : 'no');
        platform.setProperty('cache', 'yes');"""
if "platform.setProperty('hwdec'" not in content:
    content = content.replace(search_hwdec, new_hwdec)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixes applied")
