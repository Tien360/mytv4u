import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_logic = """        if (ytRes.statusCode == 200) {
          final regex = RegExp(r'\"videoRenderer\":\{\"videoId\":\"([a-zA-Z0-9_-]{11})\"');
          final match = regex.firstMatch(ytRes.body);
          if (match != null && match.group(1) != null) {
            return match.group(1);
          }
        }"""

new_logic = """        if (ytRes.statusCode == 200) {
          final regex = RegExp(r'var ytInitialData = (\{.*?\});</script>');
          final match = regex.firstMatch(ytRes.body);
          if (match != null && match.group(1) != null) {
            try {
              final data = json.decode(match.group(1)!);
              final contents = data['contents']?['twoColumnSearchResultsRenderer']?['primaryContents']?['sectionListRenderer']?['contents'] as List?;
              if (contents != null) {
                for (var section in contents) {
                  if (section['itemSectionRenderer'] != null) {
                    final items = section['itemSectionRenderer']['contents'] as List?;
                    if (items != null) {
                      for (var item in items) {
                        if (item['videoRenderer'] != null) {
                          return item['videoRenderer']['videoId'];
                        }
                      }
                    }
                  }
                }
              }
            } catch (e) {
              print('JSON parse error ytInitialData: $e');
            }
          }
          
          // Fallback regex if JSON parsing fails
          final fallbackRegex = RegExp(r'\"videoRenderer\":\{\"videoId\":\"([a-zA-Z0-9_-]{11})\"');
          final fallbackMatch = fallbackRegex.firstMatch(ytRes.body);
          if (fallbackMatch != null && fallbackMatch.group(1) != null) {
            return fallbackMatch.group(1);
          }
        }"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed YouTube parsing logic")
else:
    print("Old logic not found")
