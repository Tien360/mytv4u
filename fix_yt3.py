import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_logic = """        if (ytRes.statusCode == 200) {
          final html = ytRes.body;
          int startIndex = html.indexOf('var ytInitialData = {');
          if (startIndex != -1) {
            int endIndex = html.indexOf(';</script>', startIndex);
            if (endIndex != -1) {
              String jsonStr = html.substring(startIndex + 20, endIndex);
              try {
                final data = json.decode(jsonStr);
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
          }
          
          // No regex fallback! It hits Ads.
        }"""

text = re.sub(r'if \(ytRes\.statusCode == 200\) \{.*?return fallbackMatch\.group\(1\);\n\s*\}\n\s*\}', new_logic, text, flags=re.DOTALL)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Replaced YT parsing block with indexOf!")
