import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find _buildAudioBackground
idx = content.find("Widget _buildAudioBackground() {")
if idx != -1:
    old_child = """child: Icon(
                          Icons.music_note,
                          size: 80,
                          color: Colors.white.withValues(alpha: 0.5),
                        ),"""
    new_child = """child: widget.episodes[_currentIndex].embedUrl.startsWith('http')
                        ? ClipOval(child: CachedNetworkImage(imageUrl: widget.episodes[_currentIndex].embedUrl, fit: BoxFit.cover, width: 150, height: 150))
                        : Icon(Icons.music_note, size: 80, color: Colors.white.withValues(alpha: 0.5)),"""
    content = content.replace(old_child, new_child)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched _buildAudioBackground")
else:
    print("Could not find _buildAudioBackground")
