import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Episode construction and PlayerScreen
pattern = r"final ep = Episode\([\s\S]*?Navigator\.push"
new_content = """final ep = Episode(
        name: 'Full',
        slug: 'full',
        filename: vid,
        m3u8Url: '',
        embedUrl: '',
      );

      Navigator.push"""
content = re.sub(pattern, new_content, content)

# Remove unused Movie instance
content = re.sub(r"final movie = Movie\([\s\S]*?episodes: \[\],\n      \);", "", content)

# Fix PlayerScreen currentEpisodeIndex
content = content.replace("movieName: 'YouTube Video',", "movieName: 'YouTube Video',\n            currentEpisodeIndex: 0,")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed youtube_screen.dart")
