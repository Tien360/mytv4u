import re

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Remove imports
content = re.sub(r"import '../api/premium_resolver.dart';\n", "", content)
content = re.sub(r"import '../api/opensubtitles_api.dart';\n", "", content)
content = re.sub(r"import '../api/skip_segments_api.dart';\n", "", content)
content = re.sub(r"import 'package:webview_windows/webview_windows.dart';\n", "", content)

# Remove unused API calls
content = re.sub(r"await PremiumResolver\.fetchPremiumServer\(.*?\);", "// Removed Premium", content, flags=re.DOTALL)
content = re.sub(r"await SkipSegmentsApi\.fetchSegments\(.*?\);", "// Removed SkipSegments", content, flags=re.DOTALL)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
