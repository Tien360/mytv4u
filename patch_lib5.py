with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
i = 0
while i < len(lines):
    if "final url = _urlController.text.trim();" in lines[i]:
        # found the block
        out.append(lines[i])
        i += 1
        out.append("                          if (url.isNotEmpty) {\n")
        out.append("                            Navigator.pop(context);\n")
        out.append("                            final isYt = url.contains('youtube.com') || url.contains('youtu.be');\n")
        out.append("                            if (isYt) {\n")
        out.append("                                Navigator.push(context, MaterialPageRoute(builder: (_) => YtPlayerScreen(\n")
        out.append("                                  episodes: [Episode(name: 'YouTube', slug: 'yt', m3u8Url: url, embedUrl: '')],\n")
        out.append("                                  currentEpisodeIndex: 0, movieName: 'YouTube Video', isLive: _isLive,\n")
        out.append("                                  lazyPlaylistUrl: url.contains('list=') ? url : null,\n")
        out.append("                                )));\n")
        out.append("                            } else {\n")
        out.append("                                Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(\n")
        out.append("                                  episodes: [Episode(name: 'Stream', slug: 'stream', m3u8Url: url, embedUrl: '')],\n")
        out.append("                                  currentEpisodeIndex: 0, movieName: 'Luồng Mạng', isLive: _isLive,\n")
        out.append("                                )));\n")
        out.append("                            }\n")
        out.append("                          }\n")
        
        # skip the old block
        while i < len(lines) and "style: ElevatedButton.styleFrom(" not in lines[i]:
            i += 1
    else:
        out.append(lines[i])
        i += 1

content = "".join(out)
if "import 'yt_player_screen.dart';" not in content:
    content = content.replace("import 'player_screen.dart';", "import 'player_screen.dart';\nimport 'yt_player_screen.dart';")

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
