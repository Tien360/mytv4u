import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace uri parsing for ID in movie_detail_screen
old_parse = """final uri = Uri.tryParse(ep.m3u8Url);
            if (uri != null && uri.pathSegments.isNotEmpty) {
              // Đánh giá chất lượng từ tên file/server (vd: 2160p, 1080p, 4K)
              String textToSearch = (server.serverName + " " + ep.name).toUpperCase();
              int score = 1;
              if (textToSearch.contains('4K') || textToSearch.contains('2160')) score = 4;
              else if (textToSearch.contains('1080')) score = 3;
              else if (textToSearch.contains('720')) score = 2;
              
              premiumEps.add({
                 'id': uri.pathSegments.last,
                 'score': score,
                 'filename': ep.filename ?? ''
              });
            }"""

new_parse = """final uri = Uri.tryParse(ep.m3u8Url);
            if (uri != null) {
              String rawId = uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '');
              if (rawId.isNotEmpty) {
                // Đánh giá chất lượng từ tên file/server (vd: 2160p, 1080p, 4K)
                String textToSearch = (server.serverName + " " + ep.name).toUpperCase();
                int score = 1;
                if (textToSearch.contains('4K') || textToSearch.contains('2160')) score = 4;
                else if (textToSearch.contains('1080')) score = 3;
                else if (textToSearch.contains('720')) score = 2;
                
                premiumEps.add({
                   'id': rawId,
                   'score': score,
                   'filename': ep.filename ?? ''
                });
              }
            }"""

content = content.replace(old_parse, new_parse)
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)

# Replace in player_screen and yt_player_screen
for file in ["lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()
    old = """final uri = Uri.tryParse(ep.m3u8Url);
        if (uri != null && uri.pathSegments.isNotEmpty) {
          final id = uri.pathSegments.last;"""
    new = """final uri = Uri.tryParse(ep.m3u8Url);
        if (uri != null) {
          final id = uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '');
          if (id.isNotEmpty) {"""
    
    # Also close the extra brace
    old_end = """}).catchError((_) {});
        }
      }"""
    new_end = """}).catchError((_) {});
          }
        }
      }"""
    c = c.replace(old, new)
    if "if (id.isNotEmpty)" in c and "if (uri.pathSegments.isNotEmpty)" not in c:
        c = c.replace(old_end, new_end)
    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Fixed URI ID extraction")
