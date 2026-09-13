import 'dart:convert';
import 'package:http/http.dart' as http;

class Segment {
  final double start;
  final double end;
  Segment({required this.start, required this.end});
  @override
  String toString() => '[$start - $end]';
}

class SkipSegments {
  final Segment? recap;
  final Segment? intro;
  final Segment? outro;
  SkipSegments({this.recap, this.intro, this.outro});

  factory SkipSegments.fromJson(Map<String, dynamic> json) {
    final source = json['segments'] != null ? (json['segments'] as Map<String, dynamic>) : json;
    Segment? parseSeg(dynamic data) {
      if (data == null) return null;
      Map<String, dynamic>? mapData;
      if (data is List && data.isNotEmpty) {
        mapData = data.first as Map<String, dynamic>?;
      } else if (data is Map<String, dynamic>) {
        mapData = data;
      }
      if (mapData != null) {
        if (mapData.containsKey('start_ms') && mapData['start_ms'] != null) {
          final s = (mapData['start_ms'] as num) / 1000.0;
          final e = mapData['end_ms'] != null ? (mapData['end_ms'] as num) / 1000.0 : s + 180.0;
          return Segment(start: s, end: e);
        }
        if (mapData.containsKey('start_sec') && mapData['start_sec'] != null) {
          final s = (mapData['start_sec'] as num).toDouble();
          final e = mapData['end_sec'] != null ? (mapData['end_sec'] as num).toDouble() : s + 180.0;
          return Segment(start: s, end: e);
        }
      }
      return null;
    }
    return SkipSegments(
      recap: parseSeg(source['recap']),
      intro: parseSeg(source['intro']),
      outro: parseSeg(source['outro']),
    );
  }
}

void main() async {
  String imdbId = 'tt14688458'; // Silo
  int season = 2;
  int episode = 5;
  
  final endpoints = [
    'https://api.theintrodb.org/v3/media?imdb_id=$imdbId&season=$season&episode=$episode',
    'https://api.skipdb.tv/api/segments?imdb_id=$imdbId&season=$season&episode=$episode',
    'https://api.introdb.app/segments?imdb_id=$imdbId&season=$season&episode=$episode',
  ];

  final futures = endpoints.map((url) async {
    try {
      final res = await http.get(
        Uri.parse(url),
        headers: {
          'User-Agent': 'Mozilla/5.0',
          'X-API-Key': 'a9fb57dba1eea9bc3e660a909d838d726e3bf623d52620282013481d1f6e5377',
        }
      ).timeout(const Duration(seconds: 4));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        return SkipSegments.fromJson(data);
      }
    } catch (_) { }
    return null;
  });

  final results = await Future.wait(futures);
  
  Segment? bestIntro;
  Segment? bestOutro;
  Segment? bestRecap;

  for (var seg in results) {
    if (seg != null) {
      bestIntro ??= seg.intro;
      bestOutro ??= seg.outro;
      bestRecap ??= seg.recap;
    }
  }

  print('Final Intro: $bestIntro');
  print('Final Outro: $bestOutro');
  print('Final Recap: $bestRecap');
}
