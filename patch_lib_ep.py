import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "eps.add(Episode(\n                                      name: 'Đang tải danh sách Mix/Playlist...',\n                                      slug: v,\n                                      m3u8Url: 'https://www.youtube.com/watch?v=$v'\n                                    ));",
    "eps.add(Episode(\n                                      name: 'Đang tải danh sách Mix/Playlist...',\n                                      slug: v,\n                                      m3u8Url: 'https://www.youtube.com/watch?v=$v',\n                                      embedUrl: 'https://i.ytimg.com/vi/$v/maxresdefault.jpg'\n                                    ));"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed library_screen Episode")
