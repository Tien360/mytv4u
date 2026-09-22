import sys

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove SkipSegmentsApi
content = content.replace("import '../api/skip_segments_api.dart';", "// import skip_segments_api")
content = content.replace(
    "_currentSegments = await SkipSegmentsApi.fetchSegments(actualImdbId, season, epNum);",
    "_currentSegments = null; // await SkipSegmentsApi.fetchSegments"
)

# 2. Remove OpenSubtitlesApi
content = content.replace("import '../api/opensubtitles_api.dart';", "// import opensubtitles_api")
content = content.replace(
    "final OpenSubtitlesApi _subApi = OpenSubtitlesApi();",
    "// final OpenSubtitlesApi _subApi = OpenSubtitlesApi();"
)
content = content.replace(
    "final subs = await _subApi.searchSubtitles(",
    "final subs = <SubtitleTrack>[]; // await _subApi.searchSubtitles("
)

# 3. Remove PremiumResolver
content = content.replace("import '../api/premium_resolver.dart';", "// import premium_resolver")
content = content.replace(
    "final streams = await PremiumResolver.getVideoStream(rawId);",
    "final streams = <String>[]; // await PremiumResolver.getVideoStream"
)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Done replacements")
