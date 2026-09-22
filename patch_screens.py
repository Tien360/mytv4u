import re

for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    bad_str1 = "String rawId = uri != null ? (uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '')) : '';"
    good_str1 = "String rawId = uri != null && uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '';"
    content = content.replace(bad_str1, good_str1)
    
    bad_str2 = "final id = uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '');"
    good_str2 = "final id = uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '';"
    content = content.replace(bad_str2, good_str2)

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Reverted screens to use pathSegments.last")
