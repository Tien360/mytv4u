path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = "hasAlbumArt: _videoTracks.any((t) => t.albumart == true || t.image == true || (t.title?.toLowerCase().contains('album art') ?? false)),"
new_target = "hasAlbumArt: _videoTracks.any((t) => t.albumart == true || t.image == true || (t.title?.toLowerCase().contains('album art') ?? false) || (t.w != null && t.w! > 0)),"

text = text.replace(target, new_target)
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated album art logic")
