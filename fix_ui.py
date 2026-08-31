import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Hide _videoTracks if _isYoutube
search_vt = """                                if (_videoTracks.isNotEmpty) ...["""
new_vt = """                                if (_videoTracks.isNotEmpty && !_isYoutube) ...["""
if search_vt in content:
    content = content.replace(search_vt, new_vt)

# Show _ytQualities even if it's still loading (so user knows it's there), 
# and use a better label.
search_yt = """                                if (_ytQualities.length > 1) ...[
                                  ListTile(
                                    title: const Text('Chất lượng YouTube', style: TextStyle(color: Colors.white)),"""
new_yt = """                                if (_isYoutube) ...[
                                  ListTile(
                                    title: const Text('Chất lượng video', style: TextStyle(color: Colors.white)),
                                    subtitle: _ytQualities.length <= 1 ? const Text('Đang tải danh sách...', style: TextStyle(color: Colors.white54, fontSize: 12)) : null,"""
if search_yt in content:
    content = content.replace(search_yt, new_yt)

# Safer JSON parsing in _fetchYtQualities
search_fetch = """      final res = await Process.run(exePath, ['--no-playlist', '-J', url]);
      if (res.exitCode == 0) {
        final json = jsonDecode(res.stdout);"""
new_fetch = """      final res = await Process.run(exePath, ['--no-playlist', '-J', url]);
      if (res.exitCode == 0 || res.stdout.toString().contains('{')) {
        final stdoutStr = res.stdout.toString();
        final startIndex = stdoutStr.indexOf('{');
        if (startIndex == -1) return;
        final json = jsonDecode(stdoutStr.substring(startIndex));"""
if "startIndex == -1" not in content:
    content = content.replace(search_fetch, new_fetch)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixes applied")
