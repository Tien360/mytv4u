import 'dart:convert';
void main() {
  String jsonStr = '{"seasons": []}';
  Map<String, dynamic> seriesDetails = json.decode(jsonStr);
  
  try {
    final currentSeason = (seriesDetails['seasons'] as List).lastWhere(
      (s) => s['season_number'] > 0,
      orElse: () => null,
    );
    print('currentSeason: $currentSeason');
  } catch (e) {
    print('ERROR: $e');
  }
}
