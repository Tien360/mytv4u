import shutil
import re

# 1. Copy fresh from player_screen
shutil.copy("lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart")

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 2. Rename class
content = content.replace("PlayerScreen", "YtPlayerScreen")

# 3. Clean up Premium
content = content.replace("import '../api/premium_resolver.dart';", "// import premium")
content = content.replace("final streams = await PremiumResolver.getVideoStream(rawId);", "final streams = <String>[]; // Premium")

# 4. Clean up SkipSegments
content = content.replace("import '../api/skip_segments_api.dart';", "// import skip")
content = content.replace("_currentSegments = await SkipSegmentsApi.fetchSegments(actualImdbId, season, epNum);", "_currentSegments = null; // Skip")

# 5. Clean up OpenSubtitles
content = content.replace("import '../api/opensubtitles_api.dart';", "// import sub")
content = content.replace("final OpenSubtitlesApi _subApi = OpenSubtitlesApi();", "/* sub")
content = content.replace("final subs = await _subApi.searchSubtitles(", "*/ final subs = <SubtitleTrack>[]; // sub (")
content = re.sub(r"OpenSubtitlesApi\.fetchSubtitles\(.*?\);", "// fetchSub", content, flags=re.DOTALL)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Reset successful")
