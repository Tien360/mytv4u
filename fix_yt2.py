import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

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
          
          final fallbackRegex = RegExp(r'\"videoRenderer\":\{\"videoId\":\"([a-zA-Z0-9_-]{11})\"');
          final fallbackMatch = fallbackRegex.firstMatch(ytRes.body);
          if (fallbackMatch != null && fallbackMatch.group(1) != null) {
            return fallbackMatch.group(1);
          }
        }"""

text = re.sub(r'if \(ytRes\.statusCode == 200\) \{.*?return match\.group\(1\);\n\s*\}\n\s*\}', new_logic, text, flags=re.DOTALL)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Replaced YT parsing block!")
