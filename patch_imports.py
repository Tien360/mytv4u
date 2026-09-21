import re

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports back to avoid compile errors
content = "import '../api/premium_resolver.dart';\n" + content
content = "import '../api/opensubtitles_api.dart';\n" + content
content = "import '../api/skip_segments_api.dart';\n" + content
content = "import 'package:webview_windows/webview_windows.dart';\n" + content

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
