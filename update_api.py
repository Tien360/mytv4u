import re

with open("lib/api/sport_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_method = """  static Future<LivescoreData?> getLiveScores() async {
    try {
      final res = await http.get(Uri.parse('https://tinhlagi.pro/sport/livescore_data.json?t=${DateTime.now().millisecondsSinceEpoch}'));
      if (res.statusCode == 200) {
        final decoded = json.decode(res.body);
        return LivescoreData.fromJson(decoded);
      }
    } catch (e) {
      print('Error getting live scores: $e');
    }
    return null;
  }
}
"""

text = text.replace("}\n}", "}\n\n" + new_method)
with open("lib/api/sport_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Added getLiveScores")
